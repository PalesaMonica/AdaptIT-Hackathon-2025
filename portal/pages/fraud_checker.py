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
    
    /* Subtle Blue-Pink Accent Lines */
    .stMarkdown h1::before, .main h1::before {
        content: '' !important;
        position: absolute !important;
        top: -8px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 60% !important;
        height: 3px !important;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #1E40AF 30%, 
            #8B5CF6 50%, 
            #F472B6 70%, 
            transparent 100%) !important;
        border-radius: 2px !important;
        opacity: 0.8 !important;
    }
    
    .stMarkdown h1::after, .main h1::after {
        content: '' !important;
        position: absolute !important;
        bottom: -8px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 40% !important;
        height: 3px !important;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #3B82F6 25%, 
            #A855F7 50%, 
            #F472B6 75%, 
            transparent 100%) !important;
        border-radius: 2px !important;
        opacity: 0.6 !important;
    }
    
    /* Improved Section Headings */
    .main h2, .main h3 {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        border-left: 4px solid #3B82F6 !important;
        padding-left: 1rem !important;
        margin: 2rem 0 1rem 0 !important;
        text-shadow: none !important;
        background: linear-gradient(145deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.05)) !important;
        padding: 0.75rem 1rem !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    /* Enhanced Text Visibility */
    .main p, .main li, .main div {
        color: #1E293B !important;
        line-height: 1.7 !important;
        text-shadow: none !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    /* Stronger text for important content */
    .main strong, .main b {
        color: #0F172A !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }
    
    .feature-list {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(59, 130, 246, 0.2) !important;
        margin: 2rem 0 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .feature-list strong {
        color: #1E40AF !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }
    
    .feature-list ul {
        margin: 1rem 0 0 0 !important;
        padding-left: 1.5rem !important;
    }
    
    .feature-list li {
        color: #334155 !important;
        margin: 0.75rem 0 !important;
        line-height: 1.7 !important;
        font-size: 1rem !important;
        text-shadow: none !important;
        font-weight: 500 !important;
    }
    
    .feature-list li strong {
        color: #3B82F6 !important;
        font-weight: 700 !important;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #F472B6 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3) !important;
        letter-spacing: 0.025em !important;
        width: 100% !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1E40AF 0%, #7C3AED 50%, #EC4899 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Risk Level Styling - Updated to match blue-pink theme */
    .risk-high {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border-left: 6px solid #1E40AF !important;
        margin: 2rem 0 !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.3) !important;
        backdrop-filter: blur(8px) !important;
        animation: pulseBlue 2s infinite !important;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #8B5CF6, #A855F7) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border-left: 6px solid #7C3AED !important;
        margin: 2rem 0 !important;
        box-shadow: 0 12px 32px rgba(139, 92, 246, 0.3) !important;
        backdrop-filter: blur(8px) !important;
        animation: pulsePurple 2s infinite !important;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #C026D3, #E879F9) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border-left: 6px solid #A855F7 !important;
        margin: 2rem 0 !important;
        box-shadow: 0 12px 32px rgba(192, 38, 211, 0.3) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    @keyframes pulseBlue {
        0%, 100% { box-shadow: 0 12px 32px rgba(59, 130, 246, 0.3); }
        50% { box-shadow: 0 16px 40px rgba(59, 130, 246, 0.5), 0 0 0 4px rgba(59, 130, 246, 0.1); }
    }
    
    @keyframes pulsePurple {
        0%, 100% { box-shadow: 0 12px 32px rgba(139, 92, 246, 0.3); }
        50% { box-shadow: 0 16px 40px rgba(139, 92, 246, 0.5), 0 0 0 4px rgba(139, 92, 246, 0.1); }
    }
    
    /* Enhanced Alert Boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 12px !important;
        font-weight: 600 !important;
        text-shadow: none !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        color: #166534 !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #1E40AF !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        color: #92400E !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #DC2626 !important;
    }
    
    /* Enhanced Summary Containers */
    .analysis-container {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(59, 130, 246, 0.2) !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .analysis-container strong {
        color: #1E40AF !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    
    .analysis-container p, .analysis-container div {
        color: #334155 !important;
        font-weight: 500 !important;
    }
    
    /* Enhanced Audio Section */
    .audio-section {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.1), rgba(139, 92, 246, 0.05)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(139, 92, 246, 0.2) !important;
        margin: 2rem 0 !important;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.15) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .audio-section h3 {
        color: #6B21A8 !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    .audio-section p {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > button {
        background: linear-gradient(145deg, rgba(255,255,255,0.9), rgba(248,250,252,0.8)) !important;
        border: 2px dashed rgba(59, 130, 246, 0.4) !important;
        border-radius: 12px !important;
        color: #1E293B !important;
        font-weight: 600 !important;
        padding: 2rem !important;
        text-shadow: none !important;
    }
    
    /* Metric styling */
    .metric-container {
        background: linear-gradient(145deg, rgba(255,255,255,0.9), rgba(248,250,252,0.8)) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        text-align: center !important;
        border: 2px solid rgba(59, 130, 246, 0.2) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    /* Interactive tip cards */
    .tip-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.9), rgba(248,250,252,0.8));
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .tip-card:hover {
        transform: translateX(10px);
        background: rgba(59, 130, 246, 0.05);
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.1);
    }
    
    /* Sidebar improvements */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(248, 250, 252, 0.98), rgba(226, 232, 240, 0.95)) !important;
        backdrop-filter: blur(12px) !important;
    }
    
    .css-1d391kg .markdown-text-container {
        color: #1E293B !important;
        text-shadow: none !important;
        font-weight: 500 !important;
    }
    
    .css-1d391kg h2 {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    
    .css-1d391kg h3 {
        color: #1E40AF !important;
        font-weight: 600 !important;
    }
    
    .css-1d391kg strong {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    
    /* Progress indicator */
    .progress-step {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin: 0 5px;
        line-height: 20px;
        text-align: center;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }
    
    .progress-active {
        background: linear-gradient(45deg, #3B82F6, #8B5CF6);
        animation: pulse 1s infinite;
    }
    
    .progress-completed {
        background: #10B981;
    }
    
    .progress-pending {
        background: #9CA3AF;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Interactive Helper Functions ----------------
def create_progress_indicator(current_step, total_steps):
    """Create visual progress indicator"""
    progress_html = "<div style='text-align: center; margin: 1rem 0;'>"
    
    for i in range(1, total_steps + 1):
        if i < current_step:
            progress_html += f"<span class='progress-step progress-completed'>{i}</span>"
        elif i == current_step:
            progress_html += f"<span class='progress-step progress-active'>{i}</span>"
        else:
            progress_html += f"<span class='progress-step progress-pending'>{i}</span>"
    
    progress_html += "</div>"
    st.markdown(progress_html, unsafe_allow_html=True)

def create_interactive_stats(suspicious_count, red_flag_count, risk_score):
    """Create interactive statistics display"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(label="Suspicious Phrases", value=f"{suspicious_count}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(label="Red Flags", value=f"{red_flag_count}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(label="Risk Score", value=f"{risk_score}/100")
        st.markdown('</div>', unsafe_allow_html=True)

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
    elif risk_score >= 40:
        risk_level = "MEDIUM"
        risk_color = "risk-medium"
    else:
        risk_level = "LOW"
        risk_color = "risk-low"
    
    # Display risk score prominently
    st.markdown(f"""
    <div class="{risk_color}">
        <h2>FRAUD RISK: {risk_level}</h2>
        <h3>Risk Score: {risk_score}/100</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed analysis sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        st.markdown("**Suspicious Patterns Found**")
        
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        st.markdown("**Financial & Contact Analysis**")
        
        if patterns['financial_promises']:
            st.warning("**Financial Claims:**")
            for promise in patterns['financial_promises']:
                st.write(f"• {promise}")
        
        if metadata_issues:
            st.error("**Document Issues:**")
            for issue in metadata_issues:
                st.write(f"• {issue}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show metrics
    st.markdown("### Analysis Metrics")
    create_interactive_stats(
        len(patterns['suspicious_phrases']), 
        len(patterns['red_flags']), 
        risk_score
    )
    
    # Recommendations
    st.markdown("### Security Recommendations")
    
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
    
    # Audio alert with enhanced styling
    st.markdown('<div class="audio-section">', unsafe_allow_html=True)
    st.markdown("### Audio Risk Alert")
    st.markdown("**Listen to automated security briefing:**")
    audio_file = create_audio_alert(risk_score)
    if audio_file:
        st.audio(audio_file, format="audio/mp3")
    else:
        st.caption("Audio alert unavailable")
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    apply_legal_portal_styling()

    st.markdown("# ⚖️ Legal Document Fraud Detection")
    
    st.markdown("""
    <div class="feature-list">
        <strong>Advanced Fraud Detection System for Legal Documents</strong>
        <br><br>
        Upload your legal document and instantly receive:
        <ul>
            <li><strong>Pattern Recognition</strong> - Detect suspicious phrases and common fraud indicators</li>
            <li><strong>Risk Assessment</strong> - Get comprehensive risk scoring based on multiple factors</li>
            <li><strong>Document Analysis</strong> - Verify structural integrity and authenticity markers</li>
            <li><strong>Audio Alerts</strong> - Receive spoken security briefings about detected risks</li>
            <li><strong>Legal Guidance</strong> - Get actionable recommendations for next steps</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Initialize fraud detector
    detector = FraudDetector()

    # Load OCR model
    ocr_reader = load_ocr_model()
    if ocr_reader is None:
        st.stop()

    # File upload section
    uploaded_file = st.file_uploader(
        "Choose your legal document for fraud analysis", 
        type=SUPPORTED_FORMATS,
        help="Supported formats: PDF, JPG, PNG, WEBP (Maximum file size: 10MB)"
    )

    if uploaded_file is not None:
        # File size check
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"File too large ({uploaded_file.size/1024/1024:.1f}MB). Maximum allowed size is 10MB.")
            return

        st.success(f"Successfully uploaded: **{uploaded_file.name}** ({uploaded_file.size/1024:.1f}KB)")

        # Extract text based on file type
        with st.spinner("Extracting text from your document..."):
            extracted_text = ""
            
            if uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain" or uploaded_file.name.endswith('.txt'):
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
            word_count = len(extracted_text.split())
            char_count = len(extracted_text)
            estimated_read_time = max(1, word_count // 200)  # Average reading speed
            
            st.success("Text extraction completed successfully!")
            
            # Interactive statistics
            st.markdown("### Document Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric(label="Words", value=f"{word_count:,}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric(label="Characters", value=f"{char_count:,}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric(label="Read Time", value=f"{estimated_read_time} min")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Show a preview of extracted text
            with st.expander("Preview Extracted Text", expanded=False):
                preview_text = extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
                st.markdown(f"""
                <div style="
                    background: rgba(248, 250, 252, 0.8);
                    padding: 1.5rem;
                    border-radius: 12px;
                    border-left: 4px solid #DC2626;
                    animation: fadeIn 0.8s ease-in;
                    font-family: 'Courier New', monospace;
                    color: #334155;
                    line-height: 1.6;
                ">
                {preview_text}
                </div>
                
                <style>
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(20px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                </style>
                """, unsafe_allow_html=True)

            # Document structure verification
            st.markdown("### Document Structure Analysis")
            structure_score, structure_issues = verify_document_structure(extracted_text)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Structure Score", f"{structure_score}/45")
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                if structure_score >= 35:
                    st.success("Proper document structure")
                elif structure_score >= 20:
                    st.warning("Some structure concerns")
                else:
                    st.error("Poor document structure")
            
            if structure_issues:
                st.warning("**Structure Issues Found:**")
                for issue in structure_issues:
                    st.write(f"• {issue}")

            # Enhanced fraud detection button with progress tracking
            if st.button("Run Comprehensive Fraud Detection", type="primary"):
                progress_container = st.container()
                
                with progress_container:
                    # Step 1: Pattern Analysis
                    create_progress_indicator(1, 4)
                    with st.spinner("Analyzing suspicious patterns..."):
                        st.sleep(0.5)  # Brief pause for visual effect
                
                with progress_container:
                    # Step 2: Risk Assessment
                    create_progress_indicator(2, 4)
                    with st.spinner("Calculating risk factors..."):
                        st.sleep(0.3)
                
                with progress_container:
                    # Step 3: Document Verification
                    create_progress_indicator(3, 4)
                    with st.spinner("Verifying document authenticity..."):
                        st.sleep(0.3)
                
                with progress_container:
                    # Step 4: Report Generation
                    create_progress_indicator(4, 4)
                    with st.spinner("Generating comprehensive report..."):
                        st.sleep(0.5)
                
                # Clear progress and show results
                progress_container.empty()
                
                st.markdown("---")
                st.markdown("### Fraud Detection Analysis Results")
                
                # Success message with visual effect
                st.balloons()  # Streamlit's built-in celebration animation
                st.success("Fraud analysis completed successfully!")
                
                # Comprehensive fraud analysis
                risk_score, risk_level = display_fraud_analysis_results(detector, extracted_text)

                # Generate downloadable report
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
                
                # Additional interactive features
                st.markdown("---")
                st.markdown("### Additional Tools")
                
                tool_col1, tool_col2, tool_col3 = st.columns(3)
                
                with tool_col1:
                    st.download_button(
                        label="Download Full Report",
                        data=results_summary,
                        file_name=f"fraud_analysis_{uploaded_file.name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
                with tool_col2:
                    if st.button("Risk Breakdown", key="risk_breakdown"):
                        st.info("Detailed risk analysis:")
                        patterns = detector.analyze_text_patterns(extracted_text)
                        st.write(f"• Suspicious Phrases: {len(patterns['suspicious_phrases'])} (15 pts each)")
                        st.write(f"• Red Flags: {len(patterns['red_flags'])} (25 pts each)")
                        st.write(f"• Urgency Indicators: {len(patterns['urgency_indicators'])} (10 pts each)")
                
                with tool_col3:
                    if st.button("Security Tips", key="security_tips"):
                        st.info("Security recommendations based on analysis")
                        if risk_score >= 70:
                            st.error("Contact legal professionals immediately")
                        elif risk_score >= 40:
                            st.warning("Verify through official channels")
                        else:
                            st.success("Document appears legitimate")

        else:
            st.warning("No readable text could be extracted from your document.")
            
            # Enhanced tips section with interactive cards
            st.markdown("### Tips to improve fraud detection:")
            
            tips = [
                ("Image Quality", "Ensure the image is clear and well-lit for better text extraction"),
                ("Resolution", "Use high-resolution scans (300 DPI or higher)"),
                ("Orientation", "Make sure text is horizontal and not skewed"),
                ("Format", "Try uploading a PDF version if available"),
                ("Content", "Check that the document contains actual readable text"),
                ("Authenticity", "Look for official seals, letterheads, and proper formatting")
            ]
            
            for i, (title, description) in enumerate(tips):
                st.markdown(f"""
                <div class="tip-card" style="animation: slideIn {0.2 * (i + 1)}s ease-out;">
                    <strong style="color: #DC2626;">{title}:</strong> 
                    <span style="color: #475569;">{description}</span>
                </div>
                
                <style>
                @keyframes slideIn {{
                    from {{ opacity: 0; transform: translateX(-20px); }}
                    to {{ opacity: 1; transform: translateX(0); }}
                }}
                </style>
                """, unsafe_allow_html=True)

    # Enhanced sidebar with fraud education
    with st.sidebar:
        st.markdown("""
        ## Fraud Detection Guide

        ### **How This System Works:**
        
        **1. Upload Document**
        - Submit PDF or image files
        - Maximum file size: 10MB
        - Supports multiple formats

        **2. Text Analysis**
        - Advanced OCR extraction
        - Pattern recognition algorithms
        - Structural verification

        **3. Risk Assessment**
        - Multi-factor scoring system
        - Suspicious phrase detection
        - Document authenticity checks

        **4. Comprehensive Report**
        - Detailed risk breakdown
        - Actionable recommendations
        - Audio security briefings

        ---

        ### **Common Fraud Types:**
        - **Forged signatures**
        - **Altered dates or amounts**
        - **Fake notarization**
        - **Counterfeit letterheads**
        - **Modified terms after signing**
        - **Phishing documents**
        
        ### **Warning Signs:**
        - Pressure to sign quickly
        - Unrealistic promises
        - Poor document quality
        - Spelling/grammar errors
        - Missing official seals
        - Urgent action required

        ---

        ### **Best Practices:**
        - **Always verify** document sources
        - **Check official channels** before acting
        - **Consult legal professionals** for important documents
        - **Keep copies** of all signed documents
        - **Report suspicious** activity to authorities
        """)

    # Legal disclaimer
    st.markdown("---")
    st.caption("""
    **Legal Disclaimer:** This fraud detection tool is for informational purposes only and does not constitute legal advice. 
    Always consult with qualified legal professionals for important document verification. 
    The tool may not detect all types of fraud or may flag legitimate documents as suspicious.
    Use this tool as part of a comprehensive document verification process.
    """)

if __name__ == "__main__":
    run()