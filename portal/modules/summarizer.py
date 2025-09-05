import streamlit as st
import numpy as np
import os
from PIL import Image, ImageEnhance, ImageFilter
import io
import tempfile
from gtts import gTTS
import fitz  # PyMuPDF
import time
import pytesseract
import re
from datetime import datetime, timedelta

# ---------------- Config ----------------
SUPPORTED_FORMATS = ["jpg","jpeg","png","webp","pdf","txt","doc","docx"]
MAX_FILE_SIZE = 10*1024*1024

# ---------------- Progress Indicator ----------------
def create_progress_indicator(step, total_steps):
    """Create a visual progress indicator"""
    progress_text = f"Step {step} of {total_steps}"
    progress_percent = step / total_steps
    st.progress(progress_percent, text=progress_text)

# ---------------- Enhanced Professional Styling with Better Visibility ----------------
def apply_legal_portal_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 25%, #CBD5E1 50%, #94A3B8 75%, #64748B 100%);
        min-height: 100vh;
        color: #1E293B;
    }
    
    /* Elegant Blue-to-Pink Gradient Heading */
    .stMarkdown h1, .main h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 3.5rem !important;
        text-align: center !important;
        letter-spacing: -0.02em !important;
        margin: 2rem 0 2.5rem 0 !important;
        padding: 1.5rem 0 !important;
        position: relative !important;
        background: linear-gradient(135deg, 
            #1E40AF 0%,
            #3B82F6 15%,
            #6366F1 30%,
            #8B5CF6 45%,
            #A855F7 60%,
            #C026D3 75%,
            #E879F9 90%,
            #F472B6 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-shadow: 
            0 2px 10px rgba(30, 64, 175, 0.4),
            0 4px 20px rgba(244, 114, 182, 0.3) !important;
        filter: drop-shadow(0 0 15px rgba(139, 92, 246, 0.3)) !important;
    }
    
    .alert-box {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .alert-danger {
        background: rgba(220, 38, 38, 0.1);
        border-left-color: #DC2626;
        color: #DC2626;
    }
    
    .alert-warning {
        background: rgba(245, 158, 11, 0.1);
        border-left-color: #F59E0B;
        color: #D97706;
    }
    
    .alert-info {
        background: rgba(59, 130, 246, 0.1);
        border-left-color: #3B82F6;
        color: #1E40AF;
    }
    
    .plain-speak {
        background: linear-gradient(145deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05));
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid rgba(34, 197, 94, 0.2);
        margin: 1.5rem 0;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #166534;
    }
    
    .next-steps {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.1), rgba(139, 92, 246, 0.05));
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid rgba(139, 92, 246, 0.2);
        margin: 2rem 0;
    }
    
    .risk-indicator {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-weight: 600;
        display: flex;
        align-items: center;
    }
    
    .risk-high {
        background: rgba(239, 68, 68, 0.1);
        border: 2px solid #EF4444;
        color: #DC2626;
    }
    
    .risk-medium {
        background: rgba(245, 158, 11, 0.1);
        border: 2px solid #F59E0B;
        color: #D97706;
    }
    
    .risk-low {
        background: rgba(34, 197, 94, 0.1);
        border: 2px solid #22C55E;
        color: #166534;
    }
    
    .easy-button {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1.5rem 2rem !important;
        margin: 0.5rem 0 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.3) !important;
        width: 100% !important;
    }
    
    .easy-button:hover {
        background: linear-gradient(135deg, #16A34A 0%, #15803D 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Enhanced OCR ----------------
def preprocess_image(image):
    """Enhanced image preprocessing for better OCR results"""
    if image.mode != 'RGB': 
        image = image.convert('RGB')
    
    width, height = image.size
    if width > 2000 or height > 2000:
        ratio = min(2000/width, 2000/height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    image = ImageEnhance.Contrast(image).enhance(1.5)
    image = ImageEnhance.Sharpness(image).enhance(1.3)
    image = image.convert('L')
    image = image.filter(ImageFilter.MedianFilter(size=3))
    
    return image

def extract_text_from_image(image):
    """Extract text from image using Tesseract OCR"""
    try:
        processed = preprocess_image(image)
        text = pytesseract.image_to_string(processed, lang='eng')
        return text.strip()
    except Exception as e:
        st.error(f"OCR extraction failed: {str(e)}")
        return ""

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF using PyMuPDF"""
    try:
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        
        pdf_document.close()
        return text.strip()
    
    except Exception as e:
        st.error(f"PDF extraction failed: {str(e)}")
        return ""

# ---------------- Document Type Detection ----------------
def detect_document_type(text):
    """Detect the type of legal document"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['lease', 'tenant', 'landlord', 'rent', 'premises']):
        return "rental_agreement", "Rental/Lease Agreement"
    elif any(word in text_lower for word in ['employment', 'employee', 'employer', 'salary', 'wages']):
        return "employment", "Employment Contract"
    elif any(word in text_lower for word in ['loan', 'credit', 'debt', 'payment', 'interest']):
        return "financial", "Financial/Loan Agreement"
    elif any(word in text_lower for word in ['insurance', 'policy', 'coverage', 'claim', 'premium']):
        return "insurance", "Insurance Policy"
    elif any(word in text_lower for word in ['purchase', 'sale', 'buyer', 'seller', 'goods']):
        return "purchase", "Purchase/Sales Agreement"
    elif any(word in text_lower for word in ['service', 'provider', 'client', 'services']):
        return "service", "Service Agreement"
    else:
        return "general", "Legal Document"

# ---------------- Risk Assessment ----------------
def assess_document_risks(text, doc_type):
    """Assess potential risks in the document"""
    risks = []
    text_lower = text.lower()
    
    # High-risk patterns
    high_risk_terms = [
        'penalty', 'forfeit', 'liable', 'damages', 'breach', 'default',
        'terminate', 'evict', 'garnish', 'sue', 'court', 'legal action'
    ]
    
    medium_risk_terms = [
        'fee', 'charge', 'deposit', 'non-refundable', 'binding',
        'irrevocable', 'waive', 'surrender'
    ]
    
    # Check for high-risk terms
    high_risk_found = [term for term in high_risk_terms if term in text_lower]
    medium_risk_found = [term for term in medium_risk_terms if term in text_lower]
    
    if high_risk_found:
        risks.append({
            'level': 'high',
            'title': 'High Risk Terms Found',
            'description': f"This document contains serious consequences: {', '.join(high_risk_found[:3])}",
            'advice': 'Consider getting legal advice before signing!'
        })
    
    if medium_risk_found:
        risks.append({
            'level': 'medium',
            'title': 'Important Terms to Note',
            'description': f"Pay attention to these terms: {', '.join(medium_risk_found[:3])}",
            'advice': 'Make sure you understand these terms completely.'
        })
    
    # Check for dates and deadlines
    date_patterns = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
    if date_patterns:
        risks.append({
            'level': 'medium',
            'title': 'Important Dates Found',
            'description': f"Document contains dates: {', '.join(date_patterns[:2])}",
            'advice': 'Mark these dates on your calendar!'
        })
    
    return risks

# ---------------- Plain Language Explanations ----------------
def get_plain_language_explanation(doc_type):
    """Get plain language explanation based on document type"""
    explanations = {
        'rental_agreement': {
            'what_it_is': "This is an agreement about renting a place to live. It sets the rules between you (the tenant) and your landlord.",
            'key_things': [
                "How much rent you pay and when",
                "What happens if you're late with rent",
                "Rules about pets, guests, and noise",
                "Who pays for repairs and utilities",
                "How to end the lease properly"
            ],
            'watch_out': [
                "Penalty fees for late payments",
                "Rules that seem unfair or too strict",
                "Who is responsible for damages",
                "Notice periods for moving out"
            ]
        },
        'employment': {
            'what_it_is': "This is your job contract. It explains your work duties, pay, and the rules you need to follow at work.",
            'key_things': [
                "Your salary or hourly wage",
                "Your job duties and responsibilities",
                "Benefits like health insurance or vacation",
                "Work schedule and hours",
                "How to quit or be fired"
            ],
            'watch_out': [
                "Non-compete clauses (limits future jobs)",
                "Unpaid overtime requirements",
                "Confidentiality agreements",
                "Probation period terms"
            ]
        },
        'financial': {
            'what_it_is': "This is about borrowing or lending money. It explains how much you owe, when to pay, and what happens if you can't pay.",
            'key_things': [
                "Total amount you're borrowing",
                "Interest rate (extra money you pay)",
                "Monthly payment amount",
                "When payments are due",
                "Total amount you'll pay back"
            ],
            'watch_out': [
                "Very high interest rates",
                "Penalties for early payment",
                "What they can take if you don't pay",
                "Hidden fees or charges"
            ]
        },
        'general': {
            'what_it_is': "This is a legal agreement that creates rules and obligations between different parties.",
            'key_things': [
                "Who are the parties involved",
                "What each party must do",
                "When things must be done",
                "How much money is involved",
                "How to end the agreement"
            ],
            'watch_out': [
                "Penalties for breaking the agreement",
                "Unfair or one-sided terms",
                "Automatic renewal clauses",
                "Dispute resolution requirements"
            ]
        }
    }
    
    return explanations.get(doc_type, explanations['general'])

# ---------------- Action Steps Generator ----------------
def generate_action_steps(doc_type, risks):
    """Generate specific next steps for the user"""
    base_steps = [
        "Read this summary carefully",
        "Ask questions about anything unclear",
        "Keep a copy of the original document",
        "Note important dates in your calendar"
    ]
    
    risk_based_steps = []
    
    if any(risk['level'] == 'high' for risk in risks):
        risk_based_steps.extend([
            "Consider consulting with a lawyer",
            "Don't sign until you fully understand",
            "Ask about modifying concerning terms"
        ])
    
    if doc_type == 'rental_agreement':
        risk_based_steps.extend([
            "Inspect the property before signing",
            "Understand your tenant rights",
            "Know the eviction process in your area"
        ])
    elif doc_type == 'employment':
        risk_based_steps.extend([
            "Negotiate salary and benefits if possible",
            "Understand your employee rights",
            "Review company policies"
        ])
    elif doc_type == 'financial':
        risk_based_steps.extend([
            "Compare with other loan offers",
            "Calculate total cost of the loan",
            "Understand bankruptcy implications"
        ])
    
    return base_steps + risk_based_steps

# ---------------- Enhanced Summarizer ----------------
def simple_text_summarizer(text, max_sentences=5):
    """Simple rule-based summarizer with more sentences for clarity"""
    if not text or len(text.strip()) < 100:
        return text
    
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    
    if len(sentences) <= max_sentences:
        return text
    
    # Take more varied sentences for better coverage
    indices = [0, len(sentences)//4, len(sentences)//2, 3*len(sentences)//4, -1]
    summary_sentences = [sentences[i] for i in indices if i < len(sentences)]
    
    return '. '.join(summary_sentences) + '.'

def summarize_text(text):
    """Summarize text with fallback options"""
    if not text or len(text.strip()) < 50:
        return text
    
    try:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        max_length = 1500  # Increased for more comprehensive summary
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        summary = summarizer(text, max_length=200, min_length=80, do_sample=False)
        return summary[0]['summary_text']
    
    except ImportError:
        st.warning("Using simplified summarizer for better accessibility.")
        return simple_text_summarizer(text, max_sentences=5)
    except Exception as e:
        st.warning(f"Using simplified summarizer: {str(e)}")
        return simple_text_summarizer(text, max_sentences=5)

# ---------------- Enhanced Legal Simplification ----------------
def simplify_legal_text(text):
    """Convert legal jargon to plain language with expanded dictionary"""
    replacements = {
        # Basic legal terms
        "whereas": "because",
        "heretofore": "before now",
        "hereafter": "from now on",
        "aforementioned": "mentioned above",
        "pursuant to": "according to",
        "notwithstanding": "even though",
        "hereinafter": "from now on called",
        "therefor": "for that reason",
        "whereby": "by which",
        "thereof": "of it",
        "therein": "in it",
        "party of the first part": "first party",
        "party of the second part": "second party",
        
        # More complex terms
        "indemnify": "protect from loss",
        "covenant": "promise",
        "remedy": "solution or fix",
        "breach": "breaking the rules",
        "default": "failing to pay or do what's required",
        "liquidated damages": "pre-agreed penalty amount",
        "force majeure": "uncontrollable events (like natural disasters)",
        "arbitration": "private court hearing",
        "jurisdiction": "which court has authority",
        "severability": "if one part is invalid, the rest still applies",
        "waiver": "giving up a right",
        "consideration": "something of value exchanged",
        "amendment": "change to the agreement",
        "assignment": "transferring rights to someone else",
        "subletting": "renting to someone else while you rent",
        "lien": "legal claim on property",
        "escrow": "money held by a third party",
        "pro rata": "proportionally divided"
    }
    
    simplified = text
    for legal_term, plain_term in replacements.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(legal_term), re.IGNORECASE)
        simplified = pattern.sub(plain_term, simplified)
    
    return simplified

# ---------------- Audio with Multiple Languages ----------------
def create_audio_summary(text, language='en'):
    """Create audio file from text"""
    try:
        if not text or len(text.strip()) == 0:
            return None
            
        tts = gTTS(text=text, lang=language, slow=False)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        return tmp_file.name
    except Exception as e:
        st.error(f"Audio generation failed: {str(e)}")
        return None

def play_audio_summary(summary_text):
    """Play audio summary with multiple language options"""
    st.markdown("### Listen to Your Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**English Audio:**")
        audio_file_en = create_audio_summary(summary_text, 'en')
        if audio_file_en:
            st.audio(audio_file_en, format="audio/mp3")
        
    with col2:
        language_options = {
            "IsiZulu":"zu"
        }
        
        selected_lang = st.selectbox("Choose another language:", 
                                   ['Select a language'] + list(language_options.keys()))
        
        if selected_lang != 'Select a language':
            st.markdown(f"**{selected_lang} Audio:**")
            audio_file = create_audio_summary(summary_text, language_options[selected_lang])
            if audio_file:
                st.audio(audio_file, format="audio/mp3")

# ---------------- Main Enhanced App ----------------
def run():
    st.set_page_config(
        page_title="Legal Document Helper - Made Simple", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    apply_legal_portal_styling()

    st.markdown("# Legal Document Helper")
    st.markdown("### Making Legal Documents Easy to Understand")
    
    # Friendly introduction
    st.markdown("""
    <div class="alert-box alert-info">
        <strong>Welcome!</strong><br>
        This tool helps you understand legal documents in simple language. 
        Upload your document and we'll explain it in plain English, highlight important risks, 
        and tell you what to do next.
    </div>
    """, unsafe_allow_html=True)

    # File uploader with better instructions
    st.markdown("## Upload Your Document")
    uploaded_file = st.file_uploader(
        "Choose your document (we keep it private and secure)", 
        type=SUPPORTED_FORMATS,
        help="We support PDF files, images (JPG, PNG), and text files. Maximum size: 10MB"
    )

    if uploaded_file is not None:
        # File validation
        if uploaded_file.size > MAX_FILE_SIZE:
            st.markdown("""
            <div class="alert-box alert-danger">
                <strong>File too large!</strong><br>
                Your file is {:.1f}MB, but we can only handle files up to 10MB. 
                Try compressing your file or taking a clearer photo.
            </div>
            """.format(uploaded_file.size/1024/1024), unsafe_allow_html=True)
            return

        st.markdown(f"""
        <div class="alert-box alert-info">
            <strong>File uploaded successfully!</strong><br>
            File: {uploaded_file.name} ({uploaded_file.size/1024:.1f}KB)
        </div>
        """, unsafe_allow_html=True)

        # Extract text
        with st.spinner("Reading your document..."):
            extracted_text = ""
            
            if uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
                try:
                    extracted_text = str(uploaded_file.read(), "utf-8")
                except Exception as e:
                    st.error(f"Could not read text file: {str(e)}")
                    return
            else:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Your Document", use_container_width=True)
                    extracted_text = extract_text_from_image(image)
                except Exception as e:
                    st.error(f"Could not read image: {str(e)}")
                    return

        if extracted_text and len(extracted_text.strip()) > 0:
            
            # Show the big friendly button
            st.markdown("---")
            if st.button("Explain This Document to Me!", key="main_analyze", help="Click to get a simple explanation"):
                
                # Progress tracking
                progress_container = st.container()
                
                with progress_container:
                    create_progress_indicator(1, 5)
                    with st.spinner("Understanding your document..."):
                        # Detect document type
                        doc_type, doc_type_display = detect_document_type(extracted_text)
                        time.sleep(0.5)
                
                with progress_container:
                    create_progress_indicator(2, 5)
                    with st.spinner("Checking for important risks..."):
                        # Assess risks
                        risks = assess_document_risks(extracted_text, doc_type)
                        time.sleep(0.5)
                
                with progress_container:
                    create_progress_indicator(3, 5)
                    with st.spinner("Creating simple summary..."):
                        # Generate summaries
                        summary = summarize_text(extracted_text)
                        simplified_summary = simplify_legal_text(summary)
                        time.sleep(0.5)
                
                with progress_container:
                    create_progress_indicator(4, 5)
                    with st.spinner("Preparing your action plan..."):
                        # Get explanations and next steps
                        explanation = get_plain_language_explanation(doc_type)
                        next_steps = generate_action_steps(doc_type, risks)
                        time.sleep(0.5)
                
                with progress_container:
                    create_progress_indicator(5, 5)
                    with st.spinner("Creating audio version..."):
                        time.sleep(0.3)
                
                # Clear progress
                progress_container.empty()
                
                st.markdown("---")
                st.markdown("# Your Document Analysis")
                
                # Document type
                st.markdown(f"""
                <div class="alert-box alert-info">
                    <strong>Document Type:</strong> {doc_type_display}
                </div>
                """, unsafe_allow_html=True)
                
                # Risk assessment
                if risks:
                    st.markdown("## Important Warnings")
                    for risk in risks:
                        risk_class = f"risk-{risk['level']}"
                        st.markdown(f"""
                        <div class="risk-indicator {risk_class}">
                            <div>
                                <strong>{risk['title']}</strong><br>
                                {risk['description']}<br>
                                <em>{risk['advice']}</em>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="risk-indicator risk-low">
                        <strong>No Major Risks Found</strong><br>
                        This document appears to have standard terms, but still read carefully!
                    </div>
                    """, unsafe_allow_html=True)
                
                # Plain language explanation
                st.markdown("## What Is This Document?")
                st.markdown(f"""
                <div class="plain-speak">
                    <strong>In Simple Terms:</strong><br>
                    {explanation['what_it_is']}
                </div>
                """, unsafe_allow_html=True)
                
                # Key points
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Key Things This Document Covers:")
                    for point in explanation['key_things']:
                        st.markdown(f"• **{point}**")
                
                with col2:
                    st.markdown("### Watch Out For:")
                    for warning in explanation['watch_out']:
                        st.markdown(f"• **{warning}**")
                
                # Simplified summary
                st.markdown("## Simple Summary")
                st.markdown(f"""
                <div class="plain-speak">
                    {simplified_summary}
                </div>
                """, unsafe_allow_html=True)
                
                # Next steps
                st.markdown("## What Should You Do Next?")
                st.markdown(f"""
                <div class="next-steps">
                    <strong>Your Action Plan:</strong><br><br>
                """, unsafe_allow_html=True)
                
                for step in next_steps:
                    st.markdown(f"**{step}**")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Audio section
                play_audio_summary(simplified_summary)
                
                # Additional resources
                st.markdown("---")
                st.markdown("## Need More Help?")
                
                help_col1, help_col2, help_col3 = st.columns(3)
                
                with help_col1:
                    if st.button("Find Legal Aid", help="Find free legal help in your area"):
                        st.info("Search for 'legal aid' + your city name, or call 211 for local resources.")
                
                with help_col2:
                    if st.button("Common Questions", help="See frequently asked questions"):
                        st.info("Check our FAQ section in the sidebar for common concerns!")
                
                with help_col3:
                    if st.button("Print Summary", help="Get a printable version"):
                        st.info("Use your browser's print function to save this analysis!")
        
        else:
            st.markdown("""
            <div class="alert-box alert-warning">
                <strong>We couldn't read any text from your document.</strong><br><br>
                This might happen if:<br>
                • The image is blurry or unclear<br>
                • The text is too small or at an angle<br>
                • It's a scanned image with poor quality<br><br>
                <strong>Try:</strong><br>
                • Taking a clearer, straight-on photo<br>
                • Using a PDF version if you have one<br>
                • Making sure there's good lighting
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    run()
