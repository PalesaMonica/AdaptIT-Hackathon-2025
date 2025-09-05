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
import time

# ---------------- Config ----------------
SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "webp", "pdf", "txt"]
MAX_FILE_SIZE = 10 * 1024 * 1024

# ---------------- Professional Legal Portal Styling ----------------
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
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px rgba(126, 34, 206, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8 0%, #6d28d9 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 8px rgba(126, 34, 206, 0.25);
    }
    
    /* Risk Level Styling */
    .risk-high {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #dc2626;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #dc2626;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #d97706;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #d97706;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #16a34a;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #16a34a;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Analysis Containers */
    .analysis-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(126, 34, 206, 0.08);
    }
    
    /* Metric Containers */
    .metric-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 8px rgba(126, 34, 206, 0.08);
    }
    
    .metric-container h3 {
        font-size: 1.2rem !important;
        color: #1e40af !important;
        margin-bottom: 0.5rem;
    }
    
    /* File Uploader */
    .stFileUploader > div > button {
        background: white !important;
        border: 2px dashed #cbd5e1 !important;
        border-radius: 8px !important;
        color: #64748b !important;
        transition: all 0.2s ease;
    }
    
    .stFileUploader > div > button:hover {
        border-color: #7c3aed !important;
        background: #faf5ff !important;
    }
    
    /* Alert Boxes */
    .stSuccess {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%) !important;
        border: 1px solid #bbf7d0 !important;
        color: #166534 !important;
        border-left: 4px solid #16a34a !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%) !important;
        border: 1px solid #fde68a !important;
        color: #92400e !important;
        border-left: 4px solid #d97706 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
        border: 1px solid #fecaca !important;
        color: #dc2626 !important;
        border-left: 4px solid #dc2626 !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #f8fafc 0%, #ffffff 100%);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-weight: 600;
        color: #1e40af;
        border: 1px solid #e2e8f0;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        color: #6b7280;
        font-size: 0.9rem;
        border-top: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Fraud Detection Logic ----------------
class FraudDetector:
    def __init__(self):
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

    def analyze_text_patterns(self, text):
        results = {
            'suspicious_phrases': [],
            'red_flags': [],
            'urgency_indicators': [],
            'financial_promises': []
        }
        
        text_lower = text.lower()
        
        for phrase in self.suspicious_phrases:
            if phrase in text_lower:
                results['suspicious_phrases'].append(phrase)
        
        for flag in self.legal_red_flags:
            if flag in text_lower:
                results['red_flags'].append(flag)
        
        urgency_patterns = [r'\b(urgent|immediately|asap|deadline|expires?)\b']
        for pattern in urgency_patterns:
            matches = re.findall(pattern, text_lower)
            results['urgency_indicators'].extend(matches)
        
        financial_patterns = [r'\$[\d,]+\+?', r'\b\d+%\s*(return|profit|interest)\b']
        for pattern in financial_patterns:
            matches = re.findall(pattern, text_lower)
            results['financial_promises'].extend(matches)
        
        return results

    def calculate_risk_score(self, analysis_results):
        score = 0
        score += len(analysis_results['suspicious_phrases']) * 15
        score += len(analysis_results['red_flags']) * 25
        score += len(analysis_results['urgency_indicators']) * 10
        score += len(analysis_results['financial_promises']) * 20
        return min(score, 100)

# ---------------- Text Extraction Functions ----------------
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

# ---------------- Main Application ----------------
def run():
    st.set_page_config(
        page_title="Legal Document Fraud Detection", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    apply_legal_portal_styling()

    st.markdown("# Legal Document Fraud Detection")
    
    st.markdown("""
    <div class="feature-list">
        <h3 style="margin-top: 0; color: #1e40af;">Document Authentication Portal</h3>
        <p>Upload your legal document to detect potential fraud indicators and assess risk level using our advanced analysis system.</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize fraud detector
    detector = FraudDetector()

    # File upload section
    uploaded_file = st.file_uploader(
        "Choose a legal document to analyze", 
        type=SUPPORTED_FORMATS,
        help="Supported formats: PDF, JPG, PNG, WEBP, TXT (Max 10MB)"
    )

    if uploaded_file is not None:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error(f"File too large ({uploaded_file.size/1024/1024:.1f}MB). Maximum allowed size is 10MB.")
            return

        st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size/1024:.1f}KB)")

        # Extract text
        with st.spinner("Analyzing document..."):
            extracted_text = ""
            
            if uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
                try:
                    extracted_text = str(uploaded_file.read(), "utf-8")
                except:
                    extracted_text = uploaded_file.read().decode('utf-8', errors='ignore')
            else:
                st.warning("Image-based OCR is temporarily unavailable. Please upload PDF or text files.")
                return

        if extracted_text and len(extracted_text.strip()) > 0:
            # Run fraud detection
            patterns = detector.analyze_text_patterns(extracted_text)
            risk_score = detector.calculate_risk_score(patterns)
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = "HIGH"
                risk_class = "risk-high"
            elif risk_score >= 40:
                risk_level = "MEDIUM"
                risk_class = "risk-medium"
            else:
                risk_level = "LOW"
                risk_class = "risk-low"
            
            # Display results
            st.markdown(f"""
            <div class="{risk_class}">
                <h2>Risk Level: {risk_level}</h2>
                <h3>Risk Score: {risk_score}/100</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Show metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Suspicious Phrases", len(patterns['suspicious_phrases']))
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Red Flags", len(patterns['red_flags']))
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Risk Score", f"{risk_score}/100")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Detailed findings
            # Detailed findings
            st.markdown("### Detailed Findings")

            if any([patterns['suspicious_phrases'], patterns['red_flags'], patterns['urgency_indicators'], patterns['financial_promises']]):
                cols = st.columns(2)
                
                with cols[0]:
                    if patterns['suspicious_phrases']:
                        st.markdown("""
                        <div class="analysis-card" style="
                            background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
                            border-radius: 12px;
                            padding: 1.5rem;
                            margin-bottom: 1.5rem;
                            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.25);
                        ">
                            <h4 style="color: white; margin-top: 0; font-weight: 700; 
                                    text-shadow: 0 2px 4px rgba(0,0,0,0.2);">Suspicious Phrases</h4>
                            <div style="background: rgba(255, 255, 255, 0.95); 
                                    border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                        """, unsafe_allow_html=True)
                        for phrase in patterns['suspicious_phrases']:
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 100%);
                                padding: 0.6rem 1rem;
                                margin: 0.5rem 0;
                                border-radius: 6px;
                                border: 1px solid rgba(99, 102, 241, 0.3);
                                font-size: 0.9rem;
                                color: #1E40AF;
                                font-weight: 500;
                            ">• {phrase.title()}</div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div></div>', unsafe_allow_html=True)
                    
                    if patterns['urgency_indicators']:
                        st.markdown("""
                        <div class="analysis-card" style="
                            background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
                            border-radius: 12px;
                            padding: 1.5rem;
                            margin-bottom: 1.5rem;
                            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.25);
                        ">
                            <h4 style="color: white; margin-top: 0; font-weight: 700;
                                    text-shadow: 0 2px 4px rgba(0,0,0,0.2);">Urgency Indicators</h4>
                            <div style="background: rgba(255, 255, 255, 0.95); 
                                    border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                        """, unsafe_allow_html=True)
                        for indicator in patterns['urgency_indicators']:
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 100%);
                                padding: 0.6rem 1rem;
                                margin: 0.5rem 0;
                                border-radius: 6px;
                                border: 1px solid rgba(139, 92, 246, 0.3);
                                font-size: 0.9rem;
                                color: #3730A3;
                                font-weight: 500;
                            ">• {indicator.title()}</div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div></div>', unsafe_allow_html=True)
                
                with cols[1]:
                    if patterns['red_flags']:
                        st.markdown("""
                        <div class="analysis-card" style="
                            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
                            border-radius: 12px;
                            padding: 1.5rem;
                            margin-bottom: 1.5rem;
                            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.25);
                        ">
                            <h4 style="color: white; margin-top: 0; font-weight: 700;
                                    text-shadow: 0 2px 4px rgba(0,0,0,0.2);"> Legal Red Flags</h4>
                            <div style="background: rgba(255, 255, 255, 0.95); 
                                    border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                        """, unsafe_allow_html=True)
                        for flag in patterns['red_flags']:
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%);
                                padding: 0.6rem 1rem;
                                margin: 0.5rem 0;
                                border-radius: 6px;
                                border: 1px solid rgba(124, 58, 237, 0.3);
                                font-size: 0.9rem;
                                color: #5B21B6;
                                font-weight: 500;
                            ">• {flag.title()}</div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div></div>', unsafe_allow_html=True)
                    
                    if patterns['financial_promises']:
                        st.markdown("""
                        <div class="analysis-card" style="
                            background: linear-gradient(135deg, #8B5CF6 0%, #C026D3 100%);
                            border-radius: 12px;
                            padding: 1.5rem;
                            margin-bottom: 1.5rem;
                            box-shadow: 0 8px 25px rgba(139, 92, 246, 0.25);
                        ">
                            <h4 style="color: white; margin-top: 0; font-weight: 700;
                                    text-shadow: 0 2px 4px rgba(0,0,0,0.2);">Financial Promises</h4>
                            <div style="background: rgba(255, 255, 255, 0.95); 
                                    border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                        """, unsafe_allow_html=True)
                        for promise in patterns['financial_promises']:
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #F5F3FF 0%, #FAF5FF 100%);
                                padding: 0.6rem 1rem;
                                margin: 0.5rem 0;
                                border-radius: 6px;
                                border: 1px solid rgba(192, 38, 211, 0.3);
                                font-size: 0.9rem;
                                color: #7E22CE;
                                font-weight: 500;
                            ">• {promise}</div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div></div>', unsafe_allow_html=True)

            else:
                st.markdown("""
                <div class="analysis-card" style="
                    background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
                    border-radius: 12px;
                    padding: 2.5rem;
                    text-align: center;
                    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
                ">
                    <h4 style="color: white; margin-top: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                         No Suspicious Patterns Detected
                    </h4>
                    <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 0; margin-top: 0.5rem;">
                        No concerning phrases or patterns were found in the document analysis.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            # Recommendations
            st.markdown("### Recommendations")
            
            if risk_score >= 70:
                st.error("""
                **High Risk - Proceed with extreme caution:**
                - Consult with a legal professional
                - Verify all parties and claims
                - Do not provide personal information
                - Consider reporting to authorities
                """)
            elif risk_score >= 40:
                st.warning("""
                **Medium Risk - Verify carefully:**
                - Check document authenticity
                - Verify through official channels
                - Seek legal advice if unsure
                """)
            else:
                st.success("""
                **Low Risk - Document appears legitimate:**
                - Still review carefully
                - Keep copies for records
                - Verify important details
                """)
            
            # Text preview
            with st.expander("View Extracted Text", expanded=False):
                preview_text = extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text
                st.text_area("Extracted Text", preview_text, height=200)
                
        else:
            st.warning("Could not extract readable text from the document.")
            st.info("""
            **Tips for better results:**
            - Upload clear, high-quality documents
            - Use PDF format when possible
            - Ensure text is legible and not obscured
            - Check that the document contains actual text content
            """)

    # Sidebar information
    with st.sidebar:
        st.markdown("## About This Tool")
        st.info("""
        This tool analyzes legal documents for potential fraud indicators.
        
        **What it checks:**
        - Suspicious phrases commonly used in scams
        - Legal red flags indicating potential fraud
        - Urgency indicators and financial promises
        
        **Limitations:**
        - This is an automated tool, not legal advice
        - May produce false positives or negatives
        - Always consult legal professionals for important matters
        """)

    # Footer disclaimer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <strong>Disclaimer:</strong> This tool is for informational purposes only and does not constitute legal advice. 
        Always consult qualified legal professionals for document verification.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run()
