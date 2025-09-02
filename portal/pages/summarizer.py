import streamlit as st
import numpy as np
import os
from PIL import Image, ImageEnhance, ImageFilter
import io
import tempfile
from gtts import gTTS
import fitz  # PyMuPDF

# ---------------- Config ----------------
SUPPORTED_FORMATS = ["jpg","jpeg","png","webp","pdf","txt","doc","docx"]
MAX_FILE_SIZE = 10*1024*1024

# ---------------- Enhanced Professional Styling ----------------
def apply_legal_portal_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #1E293B 0%, #334155 25%, #475569 50%, #64748B 75%, #94A3B8 100%);
        min-height: 100vh;
        color: white;
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
            #3B82F6 0%,
            #5B9BF7 15%,
            #7BB3F8 30%,
            #9BCCF9 45%,
            #BBE4FA 60%,
            #D4A5E8 75%,
            #EC7BB8 90%,
            #F472B6 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-shadow: 
            0 2px 10px rgba(59, 130, 246, 0.3),
            0 4px 20px rgba(244, 114, 182, 0.2) !important;
        filter: drop-shadow(0 0 15px rgba(139, 92, 246, 0.2)) !important;
    }
    
    /* Subtle Blue-Pink Accent Lines */
    .stMarkdown h1::before, .main h1::before {
        content: '' !important;
        position: absolute !important;
        top: -8px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 60% !important;
        height: 2px !important;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #3B82F6 30%, 
            #8B5CF6 50%, 
            #F472B6 70%, 
            transparent 100%) !important;
        border-radius: 1px !important;
        opacity: 0.6 !important;
    }
    
    .stMarkdown h1::after, .main h1::after {
        content: '' !important;
        position: absolute !important;
        bottom: -8px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 40% !important;
        height: 2px !important;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #60A5FA 25%, 
            #A78BFA 50%, 
            #F472B6 75%, 
            transparent 100%) !important;
        border-radius: 1px !important;
        opacity: 0.4 !important;
    }
    
    /* Improved Section Headings */
    .main h2, .main h3 {
        color: #E2E8F0 !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        border-left: 4px solid #8B5CF6 !important;
        padding-left: 1rem !important;
        margin: 2rem 0 1rem 0 !important;
        text-shadow: 1px 2px 4px rgba(0,0,0,0.3) !important;
        background: rgba(139, 92, 246, 0.1) !important;
        padding: 0.75rem 1rem !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    /* Enhanced Text Visibility */
    .main p, .main li, .main div {
        color: #F1F5F9 !important;
        line-height: 1.7 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        font-weight: 400 !important;
    }
    
    /* Stronger text for important content */
    .main strong, .main b {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6) !important;
    }
    
    .feature-list {
        background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.06)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(255,255,255,0.15) !important;
        margin: 2rem 0 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .feature-list strong {
        color: #3B82F6 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.7) !important;
    }
    
    .feature-list ul {
        margin: 1rem 0 0 0 !important;
        padding-left: 1.5rem !important;
    }
    
    .feature-list li {
        color: #F1F5F9 !important;
        margin: 0.75rem 0 !important;
        line-height: 1.7 !important;
        font-size: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }
    
    .feature-list li strong {
        color: #60A5FA !important;
        font-weight: 600 !important;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #8B5CF6 0%, #F472B6 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4) !important;
        letter-spacing: 0.025em !important;
        width: 100% !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 32px rgba(139, 92, 246, 0.5) !important;
    }
    
    /* Improved Form Elements */
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.1) !important;
        color: #F8FAFC !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Enhanced Alert Boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 12px !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stSuccess {
        background: rgba(34, 197, 94, 0.15) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        color: #BBF7D0 !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #DBEAFE !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        color: #FEF3C7 !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #FECACA !important;
    }
    
    /* Enhanced Summary Containers */
    .summary-container {
        background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.06)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .summary-container strong {
        color: #3B82F6 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    
    /* Enhanced Audio Section */
    .audio-section {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.08)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        margin: 2rem 0 !important;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .audio-section h3 {
        color: #C4B5FD !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > button {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important;
        border: 2px dashed rgba(255,255,255,0.3) !important;
        border-radius: 12px !important;
        color: #F1F5F9 !important;
        font-weight: 500 !important;
        padding: 2rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)) !important;
        backdrop-filter: blur(12px) !important;
    }
    
    .css-1d391kg .markdown-text-container {
        color: #F1F5F9 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Improved spinner */
    .stSpinner {
        color: #3B82F6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- OCR ----------------
@st.cache_resource
def load_ocr_model():
    try:
        import easyocr
        return easyocr.Reader(['en'], gpu=False)
    except ImportError:
        st.error("EasyOCR not installed. Please install: pip install easyocr")
        return None
    except Exception as e:
        st.error(f"Error loading OCR model: {str(e)}")
        return None

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

def extract_text_from_image(image, ocr_reader):
    """Extract text from image using OCR"""
    if ocr_reader is None:
        return "OCR model not available"
    
    try:
        processed = preprocess_image(image)
        arr = np.array(processed)
        results = ocr_reader.readtext(arr, detail=0, paragraph=True)
        return ' '.join(results).strip()
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

# ---------------- Summarizer ----------------
def simple_text_summarizer(text, max_sentences=3):
    """Simple rule-based summarizer as fallback"""
    if not text or len(text.strip()) < 100:
        return text
    
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    
    if len(sentences) <= max_sentences:
        return text
    
    indices = [0, len(sentences)//2, -1]
    summary_sentences = [sentences[i] for i in indices if i < len(sentences)]
    
    return '. '.join(summary_sentences) + '.'

def summarize_text(text):
    """Summarize text with fallback options"""
    if not text or len(text.strip()) < 50:
        return text
    
    try:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        max_length = 1000
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        summary = summarizer(text, max_length=120, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    
    except ImportError:
        st.warning("Advanced summarizer not available. Using simple summarizer.")
        return simple_text_summarizer(text)
    except Exception as e:
        st.warning(f"Summarization error: {str(e)}. Using simple summarizer.")
        return simple_text_summarizer(text)

# ---------------- Legal Text Simplification ----------------
def simplify_legal_text(text):
    """Convert legal jargon to plain language"""
    replacements = {
        "whereas": "because",
        "heretofore": "before now",
        "hereafter": "from now on",
        "aforementioned": "mentioned above",
        "pursuant to": "according to",
        "notwithstanding": "despite",
        "hereinafter": "from now on called",
        "therefor": "for that reason",
        "whereby": "by which",
        "thereof": "of it",
        "therein": "in it",
        "party of the first part": "first party",
        "party of the second part": "second party",
    }
    
    simplified = text.lower()
    for legal_term, plain_term in replacements.items():
        simplified = simplified.replace(legal_term.lower(), plain_term)
    
    return simplified.capitalize()

# ---------------- Audio Guidance ----------------
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
    """Play audio summary"""
    st.markdown('<div class="audio-section">', unsafe_allow_html=True)
    st.markdown("### 🎧 Audio Summary")
    st.markdown("**English Audio:**")
    
    audio_file_en = create_audio_summary(summary_text, 'en')
    if audio_file_en:
        st.audio(audio_file_en, format="audio/mp3")
    else:
        st.caption("English audio unavailable")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Main App ----------------
def run():
    st.set_page_config(
        page_title="Legal Document Summarizer", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    apply_legal_portal_styling()

    st.markdown("# ⚖️ Legal Document Summarizer")
    
    st.markdown("""
    <div class="feature-list">
        <strong>Transform Complex Legal Documents into Clear Summaries</strong>
        <br><br>
        Upload your legal document and instantly receive:
        <ul>
            <li><strong>Advanced Text Extraction</strong> - Extract text from PDFs and scanned images</li>
            <li><strong>Intelligent Summarization</strong> - Get concise summaries of lengthy documents</li>
            <li><strong>Plain Language Translation</strong> - Convert legal jargon into everyday language</li>
            <li><strong>Multi-Language Audio</strong> - Listen to summaries in your preferred language</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Load OCR model
    ocr_reader = load_ocr_model()
    if ocr_reader is None:
        st.stop()

    # File uploader
    uploaded_file = st.file_uploader(
        "📁 Choose your legal document", 
        type=SUPPORTED_FORMATS,
        help="Supported formats: PDF, JPG, PNG, WEBP (Maximum file size: 10MB)"
    )

    if uploaded_file is not None:
        # Check file size
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"⚠️ File too large ({uploaded_file.size/1024/1024:.1f}MB). Maximum allowed size is 10MB.")
            return

        # Show file info
        st.success(f"✅ Successfully uploaded: **{uploaded_file.name}** ({uploaded_file.size/1024:.1f}KB)")

        # Extract text based on file type
        with st.spinner("🔍 Extracting text from your document..."):
            extracted_text = ""
            
            if uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
                try:
                    extracted_text = str(uploaded_file.read(), "utf-8")
                except Exception as e:
                    st.error(f"❌ Failed to read text file: {str(e)}")
                    return
            else:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="📄 Document Preview", use_container_width=True)
                    extracted_text = extract_text_from_image(image, ocr_reader)
                except Exception as e:
                    st.error(f"❌ Failed to process image: {str(e)}")
                    return

        # Display extracted text
        if extracted_text and len(extracted_text.strip()) > 0:
            word_count = len(extracted_text.split())
            st.info(f"📊 Successfully extracted **{word_count}** words from your document")

            # Summarization section
            if st.button("🚀 Generate Summary & Audio", type="primary"):
                with st.spinner("⚡ Creating intelligent summary..."):
                    summary = summarize_text(extracted_text)
                    simplified_summary = simplify_legal_text(summary)
                    
                    st.subheader("📝 Document Analysis Results")
                    st.success("🎉 Summary generated successfully!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('<div class="summary-container">', unsafe_allow_html=True)
                        st.markdown("**📄 Professional Summary:**")
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="summary-container">', unsafe_allow_html=True)
                        st.markdown("**💡 Plain Language Version:**")
                        st.write(simplified_summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    play_audio_summary(simplified_summary)
                    
        else:
            st.warning("⚠️ No readable text could be extracted from your document.")
            st.markdown("""
            **💡 Tips to improve text extraction:**
            - Ensure the image is clear and well-lit
            - Use high-resolution scans (300 DPI or higher)
            - Make sure text is horizontal and not skewed
            - Try uploading a PDF version if available
            - Check that the document contains actual text (not just images)
            """)

    # Enhanced sidebar instructions
    with st.sidebar:
        st.markdown("""
        ## 🛠️ How to Use This Tool

        ### **Step-by-Step Guide:**
        
        **1. 📤 Upload Your Document**
        - Click "Choose your legal document"
        - Select PDF or image files
        - Maximum file size: 10MB

        **2. 👀 Review Text Extraction**
        - Check that text was extracted correctly
        - View document preview for images

        **3. ⚡ Generate Summary**
        - Click "Generate Summary & Audio"
        - Get both professional and simplified versions

        **4. 🎧 Listen to Audio**
        - Use audio playback feature
        - Perfect for accessibility

        ---

        ### **📁 Supported File Types:**
        - **PDF**: Best for text extraction
        - **Images**: JPG, PNG, WEBP
        - **Text**: TXT files

        ---

        ### **💡 Pro Tips:**
        - **High-quality images** work best
        - **Horizontal text** extracts more accurately  
        - **PDF files** generally provide better results
        - **Clear, unblurred** documents are essential

        ---

        ### **🔧 Technical Features:**
        - AI-powered text extraction
        - Advanced summarization algorithms
        - Legal jargon simplification
        - Multi-language audio generation
        """)

if __name__ == "__main__":
    run()