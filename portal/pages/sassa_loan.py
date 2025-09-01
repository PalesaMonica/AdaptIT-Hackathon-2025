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
            summary = "DANGER: This loan appears to be a scam or predatory lending scheme."
        elif analysis["risk_level"] == "MEDIUM":
            summary = "CAUTION: This loan has concerning features that could harm your finances."
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

# ---------------- Styling ----------------
def apply_sassa_styling():
    st.markdown("""
    <style>
    /* Main container */
    .main .block-container {
        padding: 1rem 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .sassa-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(37, 99, 235, 0.2);
    }
    
    .sassa-header h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .sassa-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    /* Quick scan section */
    .quick-scan {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 3px solid #1E3A8A;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .quick-scan h2 {
        color: #1E3A8A !important;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Risk level indicators */
    .risk-high {
        background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(220, 38, 38, 0.3);
        border-left: 6px solid #7F1D1D;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(245, 158, 11, 0.3);
        border-left: 6px solid #92400E;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(5, 150, 105, 0.3);
        border-left: 6px solid #064E3B;
    }
    
    /* Analysis sections */
    .analysis-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .analysis-section h3 {
        color: #1E3A8A !important;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    
    /* Grant impact visualization */
    .grant-impact {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        text-align: center;
    }
    
    .grant-amount {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: white !important;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border: none !important;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #1E40AF 0%, #2563EB 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
    }
    
    .scan-button {
        background: linear-gradient(45deg, #059669 0%, #047857 100%) !important;
        font-size: 1.3rem !important;
        padding: 1rem 3rem !important;
        margin: 1rem auto !important;
    }
    
    /* Warning boxes */
    .warning-critical {
        background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 2px solid #1E3A8A;
    }
    
    .info-helpful {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 6px solid #1D4ED8;
    }
    
    /* Educational sections */
    .education-card {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #1E3A8A;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .education-card h4 {
        color: #1E3A8A !important;
        margin-bottom: 0.5rem;
    }
    
    /* Progress indicators */
    .scanning-progress {
        text-align: center;
        padding: 2rem;
        color: #1E40AF;
    }
    
    .progress-spinner {
        border: 4px solid #e5e7eb;
        border-top: 4px solid #1E3A8A;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 1rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .sassa-header h1 {
            font-size: 2rem;
        }
        
        .quick-scan {
            padding: 1.5rem;
        }
        
        .grant-amount {
            font-size: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Main Application ----------------
def run():
    apply_sassa_styling()
    
    # Initialize analyzer
    analyzer = SASSALoanAnalyzer()
    
    # Header
    st.markdown("""
    <div class="sassa-header">
        <h1>SASSA Loans Analysis Tool</h1>
        <p>Protect Your Grant from Predatory Lending Practices</p>
        <p><small>Comprehensive analysis of loan offers targeting social grant recipients</small></p>
    </div>
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