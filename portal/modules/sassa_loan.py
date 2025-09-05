import streamlit as st
import datetime
import re
import tempfile
import os
from gtts import gTTS

# ---------------- SASSA Loans Analysis Engine ----------------
class SASSALoanAnalyzer:
    def __init__(self):
        self.ncr_registered_lenders = [
            "African Bank", "Capitec Bank", "Standard Bank", "FNB", "ABSA",
            "Nedbank", "Old Mutual", "Discovery Bank", "TymeBank", "Finbond"
        ]
        
        self.red_flag_phrases = [
            "guaranteed approval", "no credit checks", "instant cash",
            "deduct from sassa", "grant deduction", "pension deduction",
            "100% approval", "blacklisted welcome", "unemployed welcome",
            "cash in 1 hour", "same day payout", "no paperwork",
            "sassa loans", "grant loans", "pension loans"
        ]
        
        self.high_risk_indicators = [
            "interest rate above 27.5%", "monthly service fees above R60",
            "initiation fees above R1207", "insurance not optional",
            "automatic debit order", "irrevocable mandate"
        ]
        
        self.legitimate_alternatives = {
            "Micro-lenders": ["African Bank MyWORLD", "Capitec Credit Facilities"],
            "Stokvels": ["Community savings groups", "Burial societies"],
            "Government": ["SASSA emergency loans", "Municipality hardship funds"],
            "Non-profit": ["Credit counselling services", "Financial literacy programs"]
        }
    
    def analyze_loan_document(self, document_text, loan_amount=0, monthly_payment=0, grant_amount=0):
        """Analyze loan document for SASSA-specific risks"""
        
        analysis = {
            "risk_level": "LOW",
            "risk_score": 0,
            "warnings": [],
            "violations": [],
            "recommendations": [],
            "grant_impact": {},
            "alternative_options": []
        }
        
        text_lower = document_text.lower()
        
        # Check for red flag phrases
        red_flags_found = []
        for phrase in self.red_flag_phrases:
            if phrase in text_lower:
                red_flags_found.append(phrase)
                analysis["risk_score"] += 15
        
        if red_flags_found:
            analysis["warnings"].append(f"Predatory lending language detected: {', '.join(red_flags_found[:3])}")
        
        # Check for high-risk lending practices
        high_risk_found = []
        for indicator in self.high_risk_indicators:
            if any(word in text_lower for word in indicator.split()):
                high_risk_found.append(indicator)
                analysis["risk_score"] += 10
        
        # Interest rate analysis
        interest_matches = re.findall(r'(\d+\.?\d*)\s*%', document_text)
        if interest_matches:
            max_interest = max(float(rate) for rate in interest_matches)
            if max_interest > 27.5:
                analysis["risk_score"] += 25
                analysis["violations"].append(f"Interest rate {max_interest}% exceeds NCR maximum of 27.5%")
            elif max_interest > 24:
                analysis["risk_score"] += 15
                analysis["warnings"].append(f"High interest rate: {max_interest}%")
        
        # Grant impact calculation
        if grant_amount > 0 and monthly_payment > 0:
            impact_percentage = (monthly_payment / grant_amount) * 100
            analysis["grant_impact"] = {
                "monthly_deduction": monthly_payment,
                "percentage_of_grant": impact_percentage,
                "remaining_amount": grant_amount - monthly_payment
            }
            
            if impact_percentage > 50:
                analysis["risk_score"] += 30
                analysis["violations"].append(f"Loan takes {impact_percentage:.1f}% of grant - unsustainable debt")
            elif impact_percentage > 30:
                analysis["risk_score"] += 20
                analysis["warnings"].append(f"High grant impact: {impact_percentage:.1f}%")
        
        # NCR registration check
        lender_found = False
        for lender in self.ncr_registered_lenders:
            if lender.lower() in text_lower:
                lender_found = True
                analysis["recommendations"].append(f"Verified NCR-registered lender: {lender}")
                break
        
        if not lender_found and "ncr" not in text_lower:
            analysis["risk_score"] += 20
            analysis["warnings"].append("Lender registration status unclear - verify NCR registration")
        
        # SASSA-specific checks
        if any(phrase in text_lower for phrase in ["sassa", "grant", "pension"]):
            analysis["risk_score"] += 15
            analysis["warnings"].append("Loan specifically targets social grant recipients")
        
        # Determine overall risk level
        if analysis["risk_score"] >= 60:
            analysis["risk_level"] = "HIGH"
        elif analysis["risk_score"] >= 30:
            analysis["risk_level"] = "MEDIUM"
        else:
            analysis["risk_level"] = "LOW"
        
        # Add recommendations based on risk level
        if analysis["risk_level"] == "HIGH":
            analysis["recommendations"].extend([
                "DO NOT PROCEED with this loan",
                "Report to NCR if fraudulent",
                "Seek financial counselling",
                "Consider legitimate alternatives"
            ])
        elif analysis["risk_level"] == "MEDIUM":
            analysis["recommendations"].extend([
                "Exercise extreme caution",
                "Verify lender credentials",
                "Calculate total cost carefully",
                "Consider alternatives first"
            ])
        
        # Add alternative options
        analysis["alternative_options"] = self.legitimate_alternatives
        
        return analysis
    
    def generate_plain_language_summary(self, analysis, grant_amount=0):
        """Generate easy-to-understand summary"""
        
        if analysis["risk_level"] == "HIGH":
            summary = "CAUTION: This loan appears to be a scam or predatory lending scheme."
        elif analysis["risk_level"] == "MEDIUM":
            summary = "ATTENTION: This loan has concerning features that could harm your finances."
        else:
            summary = "This loan appears to have fewer risk factors, but still verify carefully."
        
        if grant_amount > 0 and analysis["grant_impact"]:
            impact = analysis["grant_impact"]
            summary += f"\n\nGrant Impact: This loan will take R{impact['monthly_deduction']:.0f} from your R{grant_amount} grant each month ({impact['percentage_of_grant']:.1f}%), leaving you with only R{impact['remaining_amount']:.0f}."
        
        if analysis["violations"]:
            summary += f"\n\nLegal Issues: {'; '.join(analysis['violations'])}"
        
        return summary

# ---------------- Audio Support ----------------
def generate_sassa_audio(text, language='en'):
    """Generate audio explanation"""
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        st.error(f"Audio generation failed: {str(e)}")
        return None

# ---------------- Enhanced Professional Styling with Blue & Pink Theme ----------------
def apply_sassa_styling():
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
    
    /* Risk level indicators - Blue & Pink Theme */
    .risk-high {
        background: linear-gradient(145deg, rgba(30, 64, 175, 0.95), rgba(30, 58, 138, 0.9)) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.3) !important;
        border-left: 6px solid #1E3A8A !important;
        backdrop-filter: blur(8px) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .risk-medium {
        background: linear-gradient(145deg, rgba(244, 114, 182, 0.95), rgba(236, 72, 153, 0.9)) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(244, 114, 182, 0.3) !important;
        border-left: 6px solid #BE185D !important;
        backdrop-filter: blur(8px) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .risk-low {
        background: linear-gradient(145deg, rgba(34, 197, 94, 0.95), rgba(21, 128, 61, 0.9)) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.3) !important;
        border-left: 6px solid #064E3B !important;
        backdrop-filter: blur(8px) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    /* Analysis sections */
    .analysis-section {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        border-left: 5px solid #1E3A8A !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .analysis-section h3 {
        color: #1E40AF !important;
        font-size: 1.3rem !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
    }
    
    /* Grant impact visualization */
    .grant-impact {
        background: linear-gradient(145deg, rgba(30, 64, 175, 0.95), rgba(30, 58, 138, 0.9)) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.3) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .grant-impact h3 {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    /* Warning boxes - Blue & Pink Theme */
    .warning-critical {
        background: linear-gradient(145deg, rgba(30, 64, 175, 0.95), rgba(30, 58, 138, 0.9)) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.2) !important;
        backdrop-filter: blur(8px) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .info-helpful {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.95), rgba(124, 58, 237, 0.9)) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        border-left: 6px solid #7C3AED !important;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2) !important;
        backdrop-filter: blur(8px) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    /* Educational sections */
    .education-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        border-left: 5px solid #1E40AF !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .education-card h4 {
        color: #1E40AF !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
    }
    
    .education-card ul {
        margin: 1rem 0 0 0 !important;
        padding-left: 1.5rem !important;
    }
    
    .education-card li {
        color: #334155 !important;
        margin: 0.75rem 0 !important;
        line-height: 1.7 !important;
        font-size: 1rem !important;
        text-shadow: none !important;
        font-weight: 500 !important;
    }
    
    .education-card li strong {
        color: #3B82F6 !important;
        font-weight: 700 !important;
    }
    
    /* Enhanced Alert Boxes - Blue & Pink Theme */
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
        background: rgba(244, 114, 182, 0.1) !important;
        border: 1px solid rgba(244, 114, 182, 0.3) !important;
        color: #BE185D !important;
    }
    
    .stError {
        background: rgba(30, 64, 175, 0.1) !important;
        border: 1px solid rgba(30, 64, 175, 0.3) !important;
        color: #1E40AF !important;
    }
    
    /* Improved Form Elements */
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.95) !important;
        color: #1E293B !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        text-shadow: none !important;
        font-weight: 500 !important;
        backdrop-filter: blur(4px) !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.95) !important;
        color: #1E293B !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        backdrop-filter: blur(4px) !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > button {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        border: 2px dashed rgba(59, 130, 246, 0.4) !important;
        border-radius: 16px !important;
        color: #1E293B !important;
        font-weight: 600 !important;
        padding: 2rem !important;
        text-shadow: none !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > button:hover {
        border-color: #3B82F6 !important;
        background: linear-gradient(145deg, rgba(59, 130, 246, 0.05), rgba(59, 130, 246, 0.02)) !important;
    }
    
    /* Enhanced Audio Section */
    .audio-section {
        background: linear-gradient(145deg, rgba(244, 114, 182, 0.95), rgba(236, 72, 153, 0.9)) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(244, 114, 182, 0.2) !important;
        margin: 2rem 0 !important;
        box-shadow: 0 8px 32px rgba(244, 114, 182, 0.15) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .audio-section h3 {
        color: white !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .audio-section p {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    /* Progress indicators */
    .scanning-progress {
        text-align: center !important;
        padding: 2rem !important;
        color: #1E40AF !important;
        background: rgba(255,255,255,0.8) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .progress-spinner {
        border: 4px solid rgba(226, 232, 240, 0.3) !important;
        border-top: 4px solid #3B82F6 !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        animation: spin 1s linear infinite !important;
        margin: 1rem auto !important;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stMarkdown h1, .main h1 {
            font-size: 2.5rem !important;
        }
        
        .main .block-container {
            padding: 1rem 1.5rem !important;
        }
        
        .feature-list {
            padding: 1.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Helper Functions ----------------
def create_progress_indicator(step, total_steps):
    """Create a visual progress indicator"""
    progress = step / total_steps
    st.progress(progress)
    st.caption(f"Step {step} of {total_steps}")

def create_interactive_stats(grant_amount, risk_score, loan_amount=0):
    """Create interactive statistics display"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Grant Amount",
            f"R{grant_amount:,.0f}",
            help="Monthly social grant amount"
        )
    
    with col2:
        delta_color = "inverse" if risk_score > 50 else "normal"
        st.metric(
            "Risk Score",
            f"{risk_score}/100",
            delta=f"{'High' if risk_score > 60 else 'Medium' if risk_score > 30 else 'Low'} Risk",
            delta_color=delta_color,
            help="Calculated risk assessment score"
        )
    
    with col3:
        if loan_amount > 0:
            st.metric(
                "Loan Amount",
                f"R{loan_amount:,.0f}",
                help="Requested loan amount for analysis"
            )
        else:
            st.metric(
                "No Loan", 
                "R0",
                help="No loan amount specified"
            )


# ---------------- Main Application ----------------
def run():
    apply_sassa_styling()
    
    # Initialize analyzer
    analyzer = SASSALoanAnalyzer()
    
    # Header
    st.markdown("""
    <div class=" sassa-header">
        <h1>  SASSA Loans Analysis Tool</h1>
        
    """, unsafe_allow_html=True)
    
    # Quick scan section
    st.markdown("""
    <div class="quick-scan">
        <h2>Quick Safety Assessment</h2>
        <p style="font-size: 1.1rem; color: #374151;">
            Upload your loan document or paste the loan details below for immediate risk assessment and protection against grant deduction scams.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Critical warning
    st.markdown("""
    <div class="warning-critical">
        <h3>Important Notice</h3>
        <p><strong>SASSA grants cannot be used as loan collateral under South African law</strong></p>
        <ul>
            <li>Using grants as security for loans is prohibited by legislation</li>
            <li>Many loan offers targeting grant recipients violate NCR regulations</li>
            <li>Predatory lenders specifically target vulnerable grant recipients</li>
            <li>Unauthorized deductions from grants constitute financial fraud</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Loan Document Analysis")
        
        # Text input for loan details
        document_text = st.text_area(
            "Paste loan offer details:",
            height=200,
            help="Copy and paste the complete loan terms, interest rates, fees, and any other relevant details from the loan offer",
            placeholder="Paste your loan offer text here...\n\nExample: 'Quick cash loans, R2000, 24% monthly interest, deduct from SASSA grant...'"
        )
        
        # File upload option
        uploaded_file = st.file_uploader(
            "Upload loan document (PDF, image, text file):",
            type=['txt', 'pdf', 'png', 'jpg', 'jpeg'],
            help="Upload a digital copy or photograph of your loan documentation"
        )
        
        if uploaded_file is not None:
            st.success("Document uploaded successfully")
            st.info("For comprehensive analysis, please also paste the text details above")
    
    with col2:
        st.subheader("Financial Information")
        
        grant_amount = st.number_input(
            "Monthly grant amount (R):",
            min_value=0,
            value=2080,
            step=10,
            help="Enter your total monthly grant amount (SRD, Old Age Pension, Disability, etc.)"
        )
        
        loan_amount = st.number_input(
            "Requested loan amount (R):",
            min_value=0,
            value=0,
            step=100,
            help="Specify the loan amount you are considering"
        )
        
        monthly_payment = st.number_input(
            "Proposed monthly payment (R):",
            min_value=0,
            value=0,
            step=50,
            help="Indicate the monthly repayment amount specified in the offer"
        )
    
    # Analysis button
    if st.button("ANALYZE LOAN OFFER", key="scan_loan", help="Comprehensive analysis of the loan terms and conditions"):
        if document_text.strip() or uploaded_file:
            
            # Show scanning progress
            with st.spinner("Analyzing loan document for compliance and risks..."):
                st.markdown("""
                <div class="scanning-progress">
                    <div class="progress-spinner"></div>
                    <p>Evaluating lending practices...</p>
                    <p>Verifying regulatory compliance...</p>
                    <p>Assessing financial impact...</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Perform analysis
                analysis = analyzer.analyze_loan_document(
                    document_text, 
                    loan_amount=loan_amount, 
                    monthly_payment=monthly_payment, 
                    grant_amount=grant_amount
                )
                
                # Generate summary
                summary = analyzer.generate_plain_language_summary(analysis, grant_amount)
            
            # Clear progress indicator
            st.empty()
            
            # Display results based on risk level
            risk_class = f"risk-{analysis['risk_level'].lower()}"
            
            if analysis['risk_level'] == 'HIGH':
                st.markdown(f"""
                <div class="{risk_class}">
                    <h2>High Risk - Immediate Action Required</h2>
                    <p style="font-size: 1.2rem; font-weight: bold;">Risk Assessment: {analysis['risk_score']}/100</p>
                    <p>{summary}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Audio warning
                if st.button("Audio Explanation", key="audio_warning"):
                    audio_text = "High risk assessment. This loan appears to violate multiple regulatory requirements and may constitute predatory lending. Immediate consultation with financial authorities is recommended."
                    audio_file = generate_sassa_audio(audio_text)
                    if audio_file:
                        with open(audio_file, 'rb') as f:
                            audio_bytes = f.read()
                        st.audio(audio_bytes, format='audio/mp3')
                        os.unlink(audio_file)
                
            elif analysis['risk_level'] == 'MEDIUM':
                st.markdown(f"""
                <div class="{risk_class}">
                    <h2>Medium Risk - Caution Advised</h2>
                    <p style="font-size: 1.2rem; font-weight: bold;">Risk Assessment: {analysis['risk_score']}/100</p>
                    <p>{summary}</p>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div class="{risk_class}">
                    <h2>Lower Risk Profile</h2>
                    <p style="font-size: 1.2rem; font-weight: bold;">Risk Assessment: {analysis['risk_score']}/100</p>
                    <p>{summary}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Grant impact visualization
            if grant_amount > 0 and analysis['grant_impact']:
                impact = analysis['grant_impact']
                
                st.markdown("""
                <div class="grant-impact">
                    <h3>Financial Impact Analysis</h3>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Current Grant",
                        f"R{grant_amount:,.0f}",
                        help="Your monthly grant amount"
                    )
                
                with col2:
                    st.metric(
                        "Monthly Deduction",
                        f"R{impact['monthly_deduction']:,.0f}",
                        f"-{impact['percentage_of_grant']:.1f}%",
                        delta_color="inverse",
                        help="Proposed monthly loan deduction"
                    )
                
                with col3:
                    st.metric(
                        "Remaining Funds",
                        f"R{impact['remaining_amount']:,.0f}",
                        help="Available funds after loan repayment"
                    )
            
            # Detailed analysis sections
            if analysis['violations']:
                st.markdown("""
                <div class="analysis-section">
                    <h3>Regulatory Compliance Issues</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for violation in analysis['violations']:
                    st.error(f"{violation}")
            
            if analysis['warnings']:
                st.markdown("""
                <div class="analysis-section">
                    <h3>Risk Indicators</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for warning in analysis['warnings']:
                    st.warning(f"{warning}")
            
            # Recommendations
            if analysis['recommendations']:
                st.markdown("""
                <div class="analysis-section">
                    <h3>Professional Recommendations</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for rec in analysis['recommendations']:
                    if "NOT PROCEED" in rec:
                        st.error(f"{rec}")
                    else:
                        st.info(f"{rec}")
            
            # Safe alternatives
            st.markdown("""
            <div class="info-helpful">
                <h3>Alternative Financial Solutions</h3>
                <p>Consider these regulated financial alternatives instead of high-risk loans:</p>
            </div>
            """, unsafe_allow_html=True)
            
            for category, options in analysis['alternative_options'].items():
                with st.expander(f"{category}"):
                    for option in options:
                        st.write(f"• {option}")
        
        else:
            st.error("Please provide loan details or upload a document for analysis")
    
    # Educational section
    st.markdown("---")
    st.subheader("Financial Protection Guidelines")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="education-card">
            <h4>Risk Indicators to Identify</h4>
            <ul>
                <li><strong>Guaranteed approval claims</strong> - Legitimate lenders conduct proper risk assessment</li>
                <li><strong>Absence of credit checks</strong> - Regulatory compliance requires credit evaluation</li>
                <li><strong>SASSA-specific loan offers</strong> - Using social grants as security violates legislation</li>
                <li><strong>Immediate disbursement promises</strong> - Proper loan processing requires verification time</li>
                <li><strong>Advance fee requirements</strong> - Regulatory frameworks prohibit upfront payments</li>
                <li><strong>High-pressure sales tactics</strong> - Ethical lending allows for consideration periods</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="education-card">
            <h4>Characteristics of Compliant Lenders</h4>
            <ul>
                <li><strong>NCR registration</strong> - Mandatory regulatory compliance certification</li>
                <li><strong>Transparent terms</strong> - Clear disclosure of all interest rates and fees</li>
                <li><strong>Cooling-off period</strong> - Regulatory requirement for reconsideration</li>
                <li><strong>Comprehensive documentation</strong> - Detailed loan agreement specifications</li>
                <li><strong>Physical business presence</strong> - Verifiable operational addresses</li>
                <li><strong>Responsible lending assessment</strong> - Affordability evaluation requirements</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Emergency contacts
    st.markdown("""
    <div class="warning-critical">
        <h3>Regulatory Support Contacts</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div>
                <strong>National Credit Regulator (NCR)</strong><br>
                <strong>Telephone:</strong> 0860 627 627<br>
                <strong>Email:</strong> complaints@ncr.org.za
            </div>
            <div>
                <strong>SAPS Commercial Crime Unit</strong><br>
                <strong>Telephone:</strong> 10111<br>
                <strong>Purpose:</strong> Reporting financial fraud and illegal lending
            </div>
            <div>
                <strong>Debt Counselling Services</strong><br>
                <strong>Telephone:</strong> 0861 332 827<br>
                <strong>Service:</strong> Professional financial advisory services
            </div>
            <div>
                <strong>SASSA Fraud Reporting</strong><br>
                <strong>Telephone:</strong> 0800 601 011<br>
                <strong>Purpose:</strong> Grant-related fraud investigation
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Final disclaimer
    st.markdown("""
    <div class="info-helpful">
        <h4>Legal Disclaimer</h4>
        <p>This analytical tool provides educational guidance based on regulatory frameworks and should not be considered as legal or financial advice. 
        Users must independently verify all loan offers and consult qualified financial professionals before making any financial decisions. 
        Suspected regulatory violations should be reported to the appropriate authorities immediately.</p>
    </div>
    """, unsafe_allow_html=True)

# Run the application
