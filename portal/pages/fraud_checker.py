import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
import re
import datetime
from collections import Counter
import fitz  # PyMuPDF
import tempfile
from gtts import gTTS

# ---------------- Config ----------------
SUPPORTED_FORMATS = ["jpg","jpeg","png","webp","pdf","txt","doc","docx"]
MAX_FILE_SIZE = 10*1024*1024

# ---------------- Fraud Detection Rules ----------------
class FraudDetector:
    def __init__(self):
        # Suspicious patterns
        self.suspicious_phrases = [
            "guaranteed return", "risk-free investment", "act now", "limited time offer",
            "no risk", "easy money", "get rich quick", "urgent action required",
            "confidential", "wire transfer", "advance fee", "inheritance",
            "lottery winner", "tax refund", "suspended account", "verify immediately",
            "click here now", "congratulations you have won", "final notice",
            "processing fee", "handling charges", "clearance certificate"
        ]
        
        self.legal_red_flags = [
            "forged", "altered", "backdated", "unsigned", "incomplete",
            "copy", "duplicate", "amended without authorization", "falsified",
            "counterfeit", "fabricated", "modified", "tampered"
        ]
        
        # Common legitimate legal terms that should NOT be flagged
        self.legitimate_terms = [
            "whereas", "therefore", "hereafter", "pursuant", "notwithstanding",
            "covenant", "warranty", "indemnify", "jurisdiction", "consideration"
        ]

    def analyze_text_patterns(self, text):
        """Analyze text for suspicious patterns"""
        results = {
            'suspicious_phrases': [],
            'red_flags': [],
            'urgency_indicators': [],
            'financial_promises': [],
            'contact_anomalies': []
        }
        
        text_lower = text.lower()
        
        # Check for suspicious phrases
        for phrase in self.suspicious_phrases:
            if phrase in text_lower:
                results['suspicious_phrases'].append(phrase)
        
        # Check for legal red flags
        for flag in self.legal_red_flags:
            if flag in text_lower:
                results['red_flags'].append(flag)
        
        # Check for urgency indicators
        urgency_patterns = [r'\b(urgent|immediately|asap|deadline|expires?)\b', 
                          r'\b(today only|limited time|act fast|hurry)\b']
        for pattern in urgency_patterns:
            matches = re.findall(pattern, text_lower)
            results['urgency_indicators'].extend(matches)
        
        # Check for unrealistic financial promises
        financial_patterns = [r'\$[\d,]+\+?', r'\b\d+%\s*(return|profit|interest)\b']
        for pattern in financial_patterns:
            matches = re.findall(pattern, text_lower)
            results['financial_promises'].extend(matches)
        
        return results

    def check_document_metadata(self, text):
        """Check for metadata inconsistencies"""
        issues = []
        
        # Check for date inconsistencies
        date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b'
        dates = re.findall(date_pattern, text)
        
        if dates:
            try:
                current_year = datetime.datetime.now().year
                for date_str in dates:
                    # Simple check for future dates (potential red flag)
                    if any(str(year) in date_str for year in range(current_year + 2, current_year + 10)):
                        issues.append(f"Future date detected: {date_str}")
            except:
                pass
        
        # Check for multiple different contact methods (potential scam indicator)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        if len(emails) > 3:
            issues.append(f"Multiple email addresses ({len(emails)}) - verify legitimacy")
        if len(phones) > 2:
            issues.append(f"Multiple phone numbers ({len(phones)}) - verify legitimacy")
        
        return issues

    def calculate_risk_score(self, analysis_results, metadata_issues):
        """Calculate overall fraud risk score"""
        score = 0
        max_score = 100
        
        # Weight different factors
        score += len(analysis_results['suspicious_phrases']) * 15
        score += len(analysis_results['red_flags']) * 25
        score += len(analysis_results['urgency_indicators']) * 10
        score += len(analysis_results['financial_promises']) * 20
        score += len(metadata_issues) * 15
        
        return min(score, max_score)

# ---------------- Styling ----------------
def apply_fraud_detection_styling():
    st.markdown("""
    <style>
    :root {
        --security-red: #DC2626;
        --security-orange: #EA580C;
        --security-green: #059669;
        --security-blue: #2563EB;
        --security-dark: #1F2937;
    }
    .main .block-container {
        padding: 2rem;
        background: linear-gradient(135deg, #1F2937 0%, #374151 100%);
        border-radius: 10px;
        color: white;
    }
    .main h1 {
        color: #DC2626 !important;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .main h2, .main h3 {
        color: #DC2626 !important;
        border-left: 5px solid #DC2626;
        padding-left: 10px;
    }
    .stButton > button {
        background: linear-gradient(45deg, #DC2626, #EF4444) !important;
        color: white !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .risk-high {
        background: linear-gradient(45deg, #DC2626, #EF4444);
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #B91C1C;
    }
    .risk-medium {
        background: linear-gradient(45deg, #EA580C, #F97316);
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #C2410C;
    }
    .risk-low {
        background: linear-gradient(45deg, #059669, #10B981);
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #047857;
    }
    .metric-container {
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- OCR Functions ----------------
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

def preprocess_image_for_fraud_detection(image):
    """Enhanced preprocessing for fraud detection"""
    if image.mode != 'RGB': 
        image = image.convert('RGB')
    
    # Resize for better processing
    width, height = image.size
    if width > 2000 or height > 2000:
        ratio = min(2000/width, 2000/height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Enhanced preprocessing for document fraud detection
    image = ImageEnhance.Contrast(image).enhance(1.8)
    image = ImageEnhance.Sharpness(image).enhance(2.0)
    image = image.convert('L')
    image = image.filter(ImageFilter.MedianFilter(size=3))
    
    return image

def extract_text_from_image(image, ocr_reader):
    if ocr_reader is None:
        return "OCR model not available"
    
    try:
        processed = preprocess_image_for_fraud_detection(image)
        arr = np.array(processed)
        results = ocr_reader.readtext(arr, detail=0, paragraph=True)
        return ' '.join(results).strip()
    except Exception as e:
        st.error(f"OCR extraction failed: {str(e)}")
        return ""

def extract_text_from_pdf(uploaded_file):
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

# ---------------- Audio Alerts ----------------
def create_audio_alert(risk_level, language='en'):
    """Create audio alert based on risk level"""
    try:
        if risk_level >= 70:
            message = "High fraud risk detected. Please verify this document carefully with legal professionals."
        elif risk_level >= 40:
            message = "Medium fraud risk detected. Review document details thoroughly before proceeding."
        else:
            message = "Low fraud risk detected. Document appears legitimate but always verify important details."
        
        tts = gTTS(text=message, lang=language, slow=False)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        return tmp_file.name
    except Exception as e:
        return None

# ---------------- Results Display ----------------
def display_fraud_analysis_results(detector, text):
    """Display comprehensive fraud analysis results"""
    
    # Run analysis
    patterns = detector.analyze_text_patterns(text)
    metadata_issues = detector.check_document_metadata(text)
    risk_score = detector.calculate_risk_score(patterns, metadata_issues)
    
    # Risk level determination
    if risk_score >= 70:
        risk_level = "HIGH"
        risk_color = "risk-high"
        risk_emoji = "🚨"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
        risk_color = "risk-medium"
        risk_emoji = "⚠️"
    else:
        risk_level = "LOW"
        risk_color = "risk-low"
        risk_emoji = "✅"
    
    # Display risk score prominently
    st.markdown(f"""
    <div class="{risk_color}">
        <h2>{risk_emoji} FRAUD RISK: {risk_level}</h2>
        <h3>Risk Score: {risk_score}/100</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed analysis sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Suspicious Patterns Found")
        
        if patterns['suspicious_phrases']:
            st.error("**Suspicious Phrases Detected:**")
            for phrase in patterns['suspicious_phrases']:
                st.write(f"• {phrase}")
        
        if patterns['red_flags']:
            st.error("**Legal Red Flags:**")
            for flag in patterns['red_flags']:
                st.write(f"• {flag}")
        
        if patterns['urgency_indicators']:
            st.warning("**Urgency Indicators:**")
            for indicator in patterns['urgency_indicators']:
                st.write(f"• {indicator}")
    
    with col2:
        st.subheader("💰 Financial & Contact Analysis")
        
        if patterns['financial_promises']:
            st.warning("**Financial Claims:**")
            for promise in patterns['financial_promises']:
                st.write(f"• {promise}")
        
        if metadata_issues:
            st.error("**Document Issues:**")
            for issue in metadata_issues:
                st.write(f"• {issue}")
        
        # Show metrics
        st.subheader("📊 Analysis Metrics")
        col3, col4, col5 = st.columns(3)
        with col3:
            st.metric("Suspicious Phrases", len(patterns['suspicious_phrases']))
        with col4:
            st.metric("Red Flags", len(patterns['red_flags']))
        with col5:
            st.metric("Risk Score", f"{risk_score}/100")
    
    # Recommendations
    st.subheader("🛡️ Security Recommendations")
    
    if risk_score >= 70:
        st.error("""
        **HIGH RISK - DO NOT PROCEED WITHOUT VERIFICATION:**
        - This document shows multiple fraud indicators
        - Consult with a legal professional immediately
        - Verify all parties and claims independently
        - Do not provide personal information or make payments
        - Report to relevant authorities if confirmed fraudulent
        """)
    elif risk_score >= 40:
        st.warning("""
        **MEDIUM RISK - PROCEED WITH CAUTION:**
        - Verify document authenticity through official channels
        - Cross-check information with known legitimate sources
        - Seek legal advice before signing or committing
        - Verify identity of all parties involved
        """)
    else:
        st.success("""
        **LOW RISK - APPEARS LEGITIMATE:**
        - Document shows minimal fraud indicators
        - Still recommended to verify important details
        - Always read terms and conditions carefully
        - Keep copies of all signed documents
        """)
    
    # Audio alert
    st.subheader("🔊 Audio Risk Alert")
    audio_file = create_audio_alert(risk_score)
    if audio_file:
        st.audio(audio_file, format="audio/mp3")
    
    return risk_score, risk_level

# ---------------- Document Verification ----------------
def verify_document_structure(text):
    """Check document structure for legitimacy"""
    structure_score = 0
    issues = []
    
    # Check for proper document structure
    if re.search(r'\b(agreement|contract|legal document|terms|conditions)\b', text.lower()):
        structure_score += 10
    else:
        issues.append("Missing standard legal document indicators")
    
    # Check for proper formatting
    if re.search(r'\b(section|clause|paragraph|article)\s+\d+', text.lower()):
        structure_score += 15
    else:
        issues.append("Lacks proper legal document formatting")
    
    # Check for signatures/execution
    if re.search(r'\b(signature|signed|executed|witness|notary)\b', text.lower()):
        structure_score += 10
    else:
        issues.append("Missing signature or execution references")
    
    # Check for dates
    date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b'
    if re.search(date_pattern, text):
        structure_score += 10
    else:
        issues.append("Missing or unclear dates")
    
    return structure_score, issues

# ---------------- Main Application ----------------
def run():
    st.set_page_config(
        page_title="Legal Document Fraud Detection", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    apply_fraud_detection_styling()

    st.title("🛡️ Legal Document Fraud Detection")
    st.markdown("""
    **Advanced fraud detection system** for legal documents. Upload any document to:
    - 🔍 **Detect suspicious patterns** and common fraud indicators
    - ⚠️ **Identify red flags** in legal language and structure
    - 📊 **Calculate risk score** based on multiple factors
    - 🔊 **Receive audio alerts** about potential risks
    - 📋 **Get security recommendations** for next steps
    """)

    # Initialize fraud detector
    detector = FraudDetector()
    
    # Sidebar with fraud education
    with st.sidebar:
        st.header("🎓 Fraud Education")
        st.markdown("""
        ### Common Document Fraud Types:
        - **Forged signatures**
        - **Altered dates or amounts**
        - **Fake notarization**
        - **Counterfeit letterheads**
        - **Modified terms after signing**
        
        ### Warning Signs:
        - Pressure to sign quickly
        - Unrealistic promises
        - Poor document quality
        - Spelling/grammar errors
        - Missing official seals
        """)

    # Load OCR model
    ocr_reader = load_ocr_model()
    if ocr_reader is None:
        st.stop()

    # File upload section
    st.subheader("📤 Upload Document for Analysis")
    uploaded_file = st.file_uploader(
        "Choose a document to analyze for fraud indicators", 
        type=SUPPORTED_FORMATS,
        help="Upload PDF or image files. Max 10MB."
    )

    if uploaded_file is not None:
        # File size check
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"File too large ({uploaded_file.size/1024/1024:.1f}MB). Maximum size is 10MB.")
            return

        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size/1024:.1f}KB)")

        # Extract text based on file type
        with st.spinner("🔍 Analyzing document for fraud indicators..."):
            extracted_text = ""
            
            if uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
                # Handle TXT files
                try:
                    extracted_text = str(uploaded_file.read(), "utf-8")
                except Exception as e:
                    st.error(f"Failed to read text file: {str(e)}")
                    return
            else:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Document Under Analysis", use_container_width=True)
                    extracted_text = extract_text_from_image(image, ocr_reader)
                except Exception as e:
                    st.error(f"Failed to process image: {str(e)}")
                    return

        # Analyze the document
        if extracted_text and len(extracted_text.strip()) > 0:
            
            # Display extracted text in expandable section
            with st.expander("📄 View Extracted Text", expanded=False):
                st.text_area("Document Content", extracted_text, height=200, disabled=True)
            
            # Document structure verification
            st.subheader("📋 Document Structure Analysis")
            structure_score, structure_issues = verify_document_structure(extracted_text)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Structure Score", f"{structure_score}/45")
            with col2:
                if structure_score >= 35:
                    st.success("✅ Proper document structure")
                elif structure_score >= 20:
                    st.warning("⚠️ Some structure concerns")
                else:
                    st.error("🚨 Poor document structure")
            
            if structure_issues:
                st.warning("**Structure Issues Found:**")
                for issue in structure_issues:
                    st.write(f"• {issue}")

            # Run fraud detection analysis
            if st.button("🛡️ Run Fraud Detection Analysis", type="primary"):
                with st.spinner("Analyzing document for fraud patterns..."):
                    
                    # Comprehensive fraud analysis
                    st.subheader("🚨 Fraud Detection Results")
                    risk_score, risk_level = display_fraud_analysis_results(detector, extracted_text)
                    
                    # Additional analysis sections
                    st.subheader("📊 Detailed Analysis")
                    
                    # Text statistics
                    words = extracted_text.split()
                    sentences = extracted_text.split('.')
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Words", len(words))
                    with col2:
                        st.metric("Sentences", len(sentences))
                    with col3:
                        avg_word_length = np.mean([len(word) for word in words]) if words else 0
                        st.metric("Avg Word Length", f"{avg_word_length:.1f}")
                    with col4:
                        complexity = len([w for w in words if len(w) > 6]) / len(words) * 100 if words else 0
                        st.metric("Text Complexity", f"{complexity:.1f}%")
                    
                    # Keyword analysis
                    st.subheader("🔤 Keyword Frequency Analysis")
                    if words:
                        word_freq = Counter([w.lower().strip('.,!?";') for w in words if len(w) > 3])
                        top_words = word_freq.most_common(10)
                        
                        df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
                        st.dataframe(df, use_container_width=True)
                    
                    # Export results
                    st.subheader("📁 Export Analysis Results")
                    
                    results_summary = f"""
FRAUD DETECTION ANALYSIS REPORT
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Document: {uploaded_file.name}

RISK ASSESSMENT:
- Risk Level: {risk_level}
- Risk Score: {risk_score}/100
- Structure Score: {structure_score}/45

FINDINGS:
- Suspicious Phrases: {len(detector.analyze_text_patterns(extracted_text)['suspicious_phrases'])}
- Red Flags: {len(detector.analyze_text_patterns(extracted_text)['red_flags'])}
- Document Issues: {len(detector.check_document_metadata(extracted_text))}

RECOMMENDATION:
{('DO NOT PROCEED - High fraud risk' if risk_score >= 70 else 
  'PROCEED WITH CAUTION - Medium risk' if risk_score >= 40 else 
  'APPEARS LEGITIMATE - Low risk')}
                    """
                    
                    st.download_button(
                        label="📄 Download Analysis Report",
                        data=results_summary,
                        file_name=f"fraud_analysis_{uploaded_file.name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

        else:
            st.warning("⚠️ No text could be extracted from the document.")
            st.markdown("""
            **Possible reasons:**
            - Document is purely graphical
            - Image quality is too poor
            - Document is password protected
            - Unsupported file format
            
            **Try:**
            - Using a clearer, higher resolution image
            - Converting PDF to image format
            - Ensuring document contains readable text
            """)

    # Help section
    with st.expander("❓ How Does Fraud Detection Work?", expanded=False):
        st.markdown("""
        ### Our Detection Methods:
        
        **Pattern Analysis:**
        - Scans for common fraud phrases and suspicious language
        - Identifies urgency tactics and pressure techniques
        - Detects unrealistic financial promises
        
        **Document Structure:**
        - Verifies proper legal document formatting
        - Checks for standard clauses and sections
        - Validates date consistency and logic
        
        **Risk Scoring:**
        - Combines multiple risk factors
        - Weights different types of suspicious content
        - Provides actionable risk assessment
        
        **Limitations:**
        - This tool provides guidance, not legal advice
        - Always consult legal professionals for important documents
        - Human judgment is essential for final decisions
        """)

    # Legal disclaimer
    st.markdown("---")
    st.caption("""
    **Disclaimer:** This fraud detection tool is for informational purposes only and does not constitute legal advice. 
    Always consult with qualified legal professionals for important document verification. 
    The tool may not detect all types of fraud or may flag legitimate documents.
    """)
