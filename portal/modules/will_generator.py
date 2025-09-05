import streamlit as st
from fpdf import FPDF
import base64
from gtts import gTTS
import tempfile
import os
from datetime import datetime

# --- PDF GENERATOR ---
def create_will_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Add decorative border
    pdf.set_draw_color(100, 70, 180)
    pdf.set_line_width(1.0)
    pdf.rect(5, 5, 200, 287)
    
    # Title
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(70, 50, 160)
    pdf.cell(200, 20, txt="LAST WILL AND TESTAMENT", ln=True, align="C")
    pdf.ln(5)
    
    # Horizontal line
    pdf.set_draw_color(70, 50, 160)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(10)
    
    # Introduction
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, f"I, {data['name']}, Identity Number: {data.get('id_number', '__________')}, residing at {data['address']}, being of sound mind and memory, do hereby make, publish, and declare this to be my Last Will and Testament, hereby revoking all other Wills and Codicils previously made by me.")
    pdf.ln(8)

    # Marital status
    pdf.multi_cell(0, 8, f"I declare that I am {data.get('marital_status', 'single').lower()}.")
    pdf.ln(5)
    
    # Assets section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(70, 50, 160)
    pdf.cell(0, 10, txt="ARTICLE I: ESTATE ASSETS", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, "I declare that my estate consists of the following assets:")
    pdf.ln(3)
    
    for asset in data.get("assets", []):
        pdf.cell(10)  # Indentation
        pdf.multi_cell(0, 8, f"- {asset}")

    pdf.ln(5)
    
    # Beneficiaries section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(70, 50, 160)
    pdf.cell(0, 10, txt="ARTICLE II: BENEFICIARIES", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, "I hereby give, devise, and bequeath all my estate, both real and personal, of whatever kind and wherever situated, to the following beneficiaries:")
    pdf.ln(3)
    
    for i, b in enumerate(data.get("beneficiaries", []), 1):
        relationship = b.get('relationship', '')
        share = b.get('share', 'a share')
        pdf.cell(10)  # Indentation
        # Handle special characters by encoding to Latin-1
        beneficiary_text = f"{i}. {b['name']} ({relationship}): To receive {share} of my estate"
        pdf.multi_cell(0, 8, beneficiary_text.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)
    
    # Executor section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(70, 50, 160)
    pdf.cell(0, 10, txt="ARTICLE III: APPOINTMENT OF EXECUTOR", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    executor_text = f"I hereby nominate, constitute, and appoint {data['executor']} as the Executor of this my Last Will and Testament. I direct that my said Executor shall not be required to furnish any sureties on his/her official bond."
    pdf.multi_cell(0, 8, executor_text.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)
    
    # Witnesses section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(70, 50, 160)
    pdf.cell(0, 10, txt="ARTICLE IV: WITNESSES", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, "This Will shall be signed by me in the presence of two competent witnesses who shall attest thereto in my presence and in the presence of each other.")
    pdf.ln(3)
    
    for i, w in enumerate(data.get("witnesses", []), 1):
        pdf.cell(10)  # Indentation
        pdf.multi_cell(0, 8, f"Witness {i}: {w}")
    pdf.ln(10)
    
    # Closing
    pdf.multi_cell(0, 8, "IN WITNESS WHEREOF, I have hereunto set my hand this ______ day of ________________________, 20______.")
    pdf.ln(15)
    
    # Signature line
    pdf.multi_cell(0, 8, "________________________________________")
    pdf.multi_cell(0, 8, data['name'])
    pdf.multi_cell(0, 8, "Testator/Testatrix")
    pdf.ln(10)
    
    # Witness signatures
    pdf.multi_cell(0, 8, "SIGNED by the Testator/Testatrix in our presence and attested by us in the presence of the Testator/Testatrix and of each other:")
    pdf.ln(10)
    
    for i in range(2):
        pdf.multi_cell(0, 8, "________________________________________")
        pdf.multi_cell(0, 8, f"Witness {i+1}")
        pdf.multi_cell(0, 8, "Address: ____________________________________________________")
        pdf.multi_cell(0, 8, "ID Number: __________________________________________________")
        pdf.ln(5)
    
    # Notary section
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(70, 50, 160)
    pdf.cell(0, 10, txt="AFFIDAVIT OF WITNESSES", ln=True)
    pdf.ln(8)
    
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, "On this ______ day of ________________________, 20______, before me, the undersigned authority, personally appeared the Testator/Testatrix and the witnesses, known to me to be the persons described in and who executed the foregoing instrument, and they acknowledged that they executed the same as their free act and deed.")
    pdf.ln(15)
    
    pdf.multi_cell(0, 8, "________________________________________")
    pdf.multi_cell(0, 8, "Notary Public")
    pdf.multi_cell(0, 8, "My commission expires: ________________________")
    
    return pdf

def download_pdf(pdf):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            tmp.write(pdf_bytes)
            tmp.flush()
            
            with open(tmp.name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            return f'<a href="data:application/octet-stream;base64,{b64}" download="Will.pdf" style="display: inline-block; text-decoration: none; background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #F472B6 100%); color: white; padding: 15px 30px; border-radius: 12px; font-weight: 700; font-size: 1.1rem; box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3); transition: all 0.3s ease;">Download Your Will</a>'
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return ""

# --- AUDIO HELPER ---
def play_audio(text):
    try:
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            st.audio(tmp.name, format="audio/mp3")
    except Exception as e:
        st.warning(f"Audio generation failed: {str(e)}")

def apply_will_styling():
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
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #F472B6 100%) !important;
        border-radius: 10px !important;
    }
    
    .stProgress > div > div {
        background: rgba(255,255,255,0.8) !important;
        border-radius: 10px !important;
        height: 12px !important;
    }
    
    /* Form sections */
    .form-section {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        border-left: 5px solid #1E40AF !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .form-section h3 {
        color: #1E40AF !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        text-shadow: none !important;
        background: none !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Section headers with numbers */
    .section-header {
        display: flex !important;
        align-items: center !important;
        margin: 2rem 0 1rem 0 !important;
        background: linear-gradient(145deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.05)) !important;
        padding: 1rem !important;
        border-radius: 0 12px 12px 0 !important;
        border-left: 5px solid #3B82F6 !important;
    }
    
    .section-number {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
        color: white !important;
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-right: 15px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .section-header h3 {
        color: #0F172A !important;
        font-weight: 700 !important;
        margin: 0 !important;
        font-size: 1.5rem !important;
        background: none !important;
        border: none !important;
        padding: 0 !important;
    }
    
    /* Awareness cards */
    .awareness-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        border-left: 5px solid #1E40AF !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05) !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.3s ease !important;
    }
    
    .awareness-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.15) !important;
    }
    
    .info-point {
        display: flex !important;
        align-items: flex-start !important;
        margin-bottom: 0 !important;
    }
    
    .info-icon {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
        color: white !important;
        min-width: 35px !important;
        height: 35px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-right: 15px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        flex-shrink: 0 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .info-point h4 {
        color: #1E40AF !important;
        margin: 0 0 0.5rem 0 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    .info-point p {
        color: #334155 !important;
        margin: 0 !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }
    
    /* Beneficiary forms */
    .beneficiary-form {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.08), rgba(139, 92, 246, 0.05)) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        margin: 1rem 0 !important;
        border: 2px solid rgba(139, 92, 246, 0.2) !important;
        backdrop-filter: blur(4px) !important;
    }
    
    /* Success card */
    .success-card {
        background: linear-gradient(145deg, rgba(30, 64, 175, 0.95), rgba(30, 58, 138, 0.9)) !important;
        color: white !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 2rem 0 !important;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.2) !important;
        backdrop-filter: blur(8px) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        border-left: 6px solid #1E3A8A !important;
    }
    
    .success-card h3 {
        color: white !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
        background: none !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .success-card p, .success-card ul, .success-card li {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
        line-height: 1.6 !important;
    }
    
    .success-card strong, .success-card b {
        color: white !important;
        font-weight: 700 !important;
    }
    
    /* Enhanced Form Elements */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(255,255,255,0.95) !important;
        color: #1E293B !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        text-shadow: none !important;
        font-weight: 500 !important;
        backdrop-filter: blur(4px) !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        font-weight: 600 !important;
        color: #1E293B !important;
        text-shadow: none !important;
        background: rgba(255,255,255,0.8) !important;
        padding: 0.75rem !important;
        border-radius: 8px !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        margin: 0.5rem 0 !important;
        display: block !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(4px) !important;
    }
    
    .stCheckbox > label:hover {
        border-color: #3B82F6 !important;
        background: rgba(59, 130, 246, 0.05) !important;
    }
    
    /* Enhanced Alert Boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 12px !important;
        font-weight: 600 !important;
        text-shadow: none !important;
        backdrop-filter: blur(8px) !important;
        margin: 1rem 0 !important;
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
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stMarkdown h1, .main h1 {
            font-size: 2.5rem !important;
        }
        
        .main .block-container {
            padding: 1rem 1.5rem !important;
        }
        
        .form-section, .awareness-card {
            padding: 1.5rem !important;
        }
        
        .section-number {
            width: 35px !important;
            height: 35px !important;
            font-size: 1rem !important;
        }
        
        .info-icon {
            min-width: 30px !important;
            height: 30px !important;
            font-size: 0.9rem !important;
        }
        
        .section-header {
            flex-direction: column !important;
            text-align: center !important;
            gap: 1rem !important;
        }
        
        .section-number {
            margin-right: 0 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- run APP ---
def run():
    # Apply consistent styling
    apply_will_styling()

    # --- SESSION STATE ---
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}
    if "beneficiaries" not in st.session_state:
        st.session_state.beneficiaries = []
    if "witnesses" not in st.session_state:
        st.session_state.witnesses = []

    # --- HEADER ---
    st.markdown('# South African Will Generator')
    st.markdown("### Create Your Legal Will in Minutes")
    st.markdown("*Professional will generation tool for South African law*")
    st.markdown("---")
    
    # Progress indicator
    st.progress(st.session_state.step / 5)
    st.caption(f"Step {st.session_state.step} of 5")

    # --- STEP 1: Awareness ---
    if st.session_state.step == 1:
        st.markdown('<div class="section-header"><div class="section-number">1</div><h3>Why You Need a Will</h3></div>', unsafe_allow_html=True)
        
        awareness_points = [
            {
                "title": "Lack of Awareness & Understanding",
                "content": "Without a will, your family may face financial limbo. South African intestate succession laws decide who inherits, which might not align with your wishes."
            },
            {
                "title": "Belief in Insufficient Assets",
                "content": "Even if you only own a car, furniture, or a bank account — a will ensures your wishes are followed and prevents disputes among family members."
            },
            {
                "title": "Procrastination",
                "content": "Most people delay making a will. This tool helps you complete one in less than 10 minutes, giving you peace of mind."
            },
            {
                "title": "Not Knowing Where to Start",
                "content": "We guide you step by step through the entire process. No legal training needed."
            },
            {
                "title": "Perceived High Costs",
                "content": "This tool is completely free. All you need is to print and sign in front of two witnesses."
            },
            {
                "title": "Emotional Barriers",
                "content": "Making a will is an act of love and protection for your family."
            }
        ]
        
        for i, point in enumerate(awareness_points):
            st.markdown(f'''
            <div class="awareness-card">
                <div class="info-point">
                    <div class="info-icon">{i+1}</div>
                    <div>
                        <h4>{point['title']}</h4>
                        <p>{point['content']}</p>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Create My Will", key="start_btn", use_container_width=True):
                st.session_state.step = 2
                st.rerun()

    # --- STEP 2: Assets ---
    elif st.session_state.step == 2:
        st.markdown('<div class="section-header"><div class="section-number">2</div><h3>Select Your Assets</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        assets_options = [
            "Residential Property", "Vehicle", "Bank Accounts", 
            "Investments", "Retirement Funds", "Life Insurance",
            "Personal Possessions", "Business Interests", "Digital Assets"
        ]
        
        selected_assets = []
        cols = st.columns(3)
        for i, asset in enumerate(assets_options):
            with cols[i % 3]:
                if st.checkbox(asset, key=f"asset_{i}"):
                    selected_assets.append(asset)
        
        other_asset = st.text_input("Other assets not listed above:")
        if other_asset:
            selected_assets.append(other_asset)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue", key="assets_btn", use_container_width=True):
                st.session_state.form_data["assets"] = selected_assets
                st.session_state.step = 3
                st.rerun()

    # --- STEP 3: Beneficiaries ---
    elif st.session_state.step == 3:
        st.markdown('<div class="section-header"><div class="section-number">3</div><h3>Add Beneficiaries</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        st.info("A beneficiary is someone who will receive part of your estate. You can add multiple beneficiaries.")
        
        # Form to add a new beneficiary
        with st.form("beneficiary_form"):
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Full Name")
                relationship = st.selectbox("Relationship", 
                                          ["Spouse", "Child", "Parent", "Sibling", "Other Relative", "Friend", "Charity"])
            with cols[1]:
                share = st.text_input("Share of Estate", help="E.g., '50%', 'the remainder', 'my car'")
                if relationship == "Other Relative":
                    relationship = st.text_input("Specify relationship")
            
            add_beneficiary = st.form_submit_button("Add Beneficiary")
            
            if add_beneficiary and name:
                new_beneficiary = {
                    "name": name,
                    "relationship": relationship,
                    "share": share if share else "a share"
                }
                st.session_state.beneficiaries.append(new_beneficiary)
                st.success(f"Added {name} as a beneficiary")
                st.rerun()
        
        # Display current beneficiaries
        if st.session_state.beneficiaries:
            st.markdown("### Current Beneficiaries")
            for i, beneficiary in enumerate(st.session_state.beneficiaries):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                    <div class="beneficiary-form">
                        <strong>{beneficiary['name']}</strong> ({beneficiary['relationship']}) - To receive: {beneficiary['share']}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.beneficiaries.pop(i)
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue", key="beneficiaries_btn", use_container_width=True) and st.session_state.beneficiaries:
                st.session_state.form_data["beneficiaries"] = st.session_state.beneficiaries
                st.session_state.step = 4
                st.rerun()
            elif not st.session_state.beneficiaries:
                st.warning("Please add at least one beneficiary before continuing")

    # --- STEP 4: Executor ---
    elif st.session_state.step == 4:
        st.markdown('<div class="section-header"><div class="section-number">4</div><h3>Appoint an Executor</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        st.info("The executor is responsible for carrying out the instructions in your will and managing your estate.")
        
        executor_name = st.text_input("Executor's Full Name")
        executor_contact = st.text_input("Executor's Contact Information")
        alternate_executor = st.text_input("Alternate Executor (optional)", 
                                         help="Someone to serve as executor if your first choice is unable to")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue", key="executor_btn", use_container_width=True) and executor_name:
                st.session_state.form_data["executor"] = f"{executor_name} ({executor_contact})" if executor_contact else executor_name
                if alternate_executor:
                    st.session_state.form_data["executor"] += f" with {alternate_executor} as alternate"
                st.session_state.step = 5
                st.rerun()
            elif not executor_name:
                st.warning("Please appoint an executor before continuing")

    # --- STEP 5: Witnesses + Generate Will ---
    elif st.session_state.step == 5:
        st.markdown('<div class="section-header"><div class="section-number">5</div><h3>Final Details</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        
        # Personal information
        cols = st.columns(2)
        with cols[0]:
            name = st.text_input("Your Full Name", value=st.session_state.form_data.get("name", ""))
            id_number = st.text_input("Your ID Number (optional)")
        with cols[1]:
            address = st.text_input("Your Residential Address", value=st.session_state.form_data.get("address", ""))
            marital_status = st.selectbox("Marital Status", 
                                        ["Single", "Married", "Divorced", "Widowed", "Life Partnership"])
        
        # Witnesses
        st.markdown("### Witnesses")
        st.info("Your will must be signed in the presence of two competent witnesses who are not beneficiaries.")
        
        witness_cols = st.columns(2)
        witnesses = []
        for i in range(2):
            with witness_cols[i]:
                st.subheader(f"Witness {i+1}")
                witness_name = st.text_input(f"Witness {i+1} Full Name", key=f"witness_{i}_name")
                witness_id = st.text_input(f"Witness {i+1} ID Number (optional)", key=f"witness_{i}_id")
                witness_address = st.text_input(f"Witness {i+1} Address", key=f"witness_{i}_address")
                if witness_name:
                    witnesses.append(witness_name)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Generate My Will", key="generate_btn", use_container_width=True) and name and address and len(witnesses) >= 2:
                st.session_state.form_data["name"] = name
                st.session_state.form_data["address"] = address
                st.session_state.form_data["id_number"] = id_number
                st.session_state.form_data["marital_status"] = marital_status
                st.session_state.form_data["witnesses"] = witnesses
                
                try:
                    pdf = create_will_pdf(st.session_state.form_data)
                    
                    st.markdown("""
                    <div class="success-card">
                        <h3>Your will has been generated successfully!</h3>
                        
                        <p><strong>Next Steps:</strong></p>
                        <ol style="line-height:1.7; color: white;">
                            <li>Download and print your will</li>
                            <li>Sign it in the presence of two competent witnesses</li>
                            <li>Have your witnesses sign in your presence and in each other's presence</li>
                            <li>Store it in a safe place and inform your executor of its location</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Center the download button
                    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
                    with col_dl2:
                        st.markdown(f'<div style="text-align: center; margin: 2rem 0;">{download_pdf(pdf)}</div>', unsafe_allow_html=True)
                    
                    play_audio("Your will has been successfully generated. Please remember to print it and sign in front of two witnesses.")
                except Exception as e:
                    st.error(f"Error generating will: {str(e)}")
            elif not (name and address):
                st.warning("Please enter your name and address")
            elif len(witnesses) < 2:
                st.warning("Please provide at least two witnesses")

if __name__ == "__main__":
    run()
