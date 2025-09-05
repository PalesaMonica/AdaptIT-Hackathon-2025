import streamlit as st
import datetime
from fpdf import FPDF
import tempfile
import os
from gtts import gTTS
import base64

# ---------------- Config ----------------
class WillGenerator:
    def __init__(self):
        self.will_data = {}
        self.template_path = "will_templates"
        
    def create_simple_will_template(self, data):
        """Create a simple will document"""
        
        will_text = f"""
LAST WILL AND TESTAMENT

I, {data.get('full_name', '[NAME]')}, of {data.get('address', '[ADDRESS]')}, South Africa, 
being of sound mind and disposing memory, do hereby make, publish and declare this to be my Last Will and Testament, 
hereby revoking all former wills and codicils by me at any time heretofore made.

ARTICLE I - FAMILY STATUS
I am {data.get('marital_status', '[STATUS]')}. {'I have ' + str(data.get('num_children', 0)) + ' child(ren).' if data.get('num_children', 0) > 0 else 'I have no children.'}

ARTICLE II - DEBTS AND FUNERAL EXPENSES
I direct that all my just debts, funeral expenses, and the expenses of administering my estate be paid as soon as practicable after my death.

ARTICLE III - SPECIFIC BEQUESTS
{self._format_specific_bequests(data.get('specific_bequests', []))}

ARTICLE IV - RESIDUARY ESTATE
I give, devise and bequeath all the rest, residue and remainder of my estate, both real and personal, of whatsoever kind and wheresoever situated, to {data.get('primary_beneficiary', '[BENEFICIARY]')}.

ARTICLE V - ALTERNATE BENEFICIARY
In the event that {data.get('primary_beneficiary', '[BENEFICIARY]')} predeceases me or is unable to inherit, I give my entire estate to {data.get('alternate_beneficiary', '[ALTERNATE BENEFICIARY]')}.

ARTICLE VI - EXECUTOR
I hereby nominate and appoint {data.get('executor_name', '[EXECUTOR]')} of {data.get('executor_address', '[EXECUTOR ADDRESS]')} as the Executor of this my Last Will and Testament.

In the event that {data.get('executor_name', '[EXECUTOR]')} is unable or unwilling to serve, I nominate {data.get('alternate_executor', '[ALTERNATE EXECUTOR]')} as alternate Executor.

ARTICLE VII - POWERS OF EXECUTOR
I grant to my Executor full power and authority to:
- Sell, transfer, or dispose of any property in my estate
- Pay all debts and expenses
- Distribute assets according to this Will
- Engage legal and financial professionals as needed

ARTICLE VIII - GUARDIANSHIP (if applicable)
{self._format_guardianship_clause(data)}

IN WITNESS WHEREOF, I have hereunto set my hand and seal this {data.get('date', datetime.date.today().strftime('%d day of %B, %Y'))}.

TESTATOR:
_________________________________
{data.get('full_name', '[NAME]')}

WITNESSES:
We, the undersigned, being at least two in number, each being above the age of 14 years, do hereby certify that the above-named Testator signed this Will in our presence, and that we, in the Testator's presence and in the presence of each other, have signed our names as witnesses hereto.

Witness 1:
_________________________________
Name: {data.get('witness1_name', '[WITNESS 1 NAME]')}
Address: {data.get('witness1_address', '[WITNESS 1 ADDRESS]')}
Signature: _________________________
Date: ____________________________

Witness 2:
_________________________________
Name: {data.get('witness2_name', '[WITNESS 2 NAME]')}
Address: {data.get('witness2_address', '[WITNESS 2 ADDRESS]')}
Signature: _________________________
Date: ____________________________

COMMISSIONER OF OATHS (Optional but Recommended):
I certify that the deponent has acknowledged that he/she knows and understands the contents of this affidavit which was signed and sworn to before me at _____________ on this _____ day of _______, 2025, and that the Regulations contained in Government Notice R1258 of 21 July 1972 have been complied with.

_________________________________
COMMISSIONER OF OATHS
Full Names: _____________________
Designation: ____________________
Address: _______________________
"""
        return will_text
    
    def _format_specific_bequests(self, bequests):
        if not bequests:
            return "I make no specific bequests at this time."
        
        text = "I make the following specific bequests:\n"
        for i, bequest in enumerate(bequests, 1):
            text += f"{i}. I give {bequest.get('item', '')} to {bequest.get('beneficiary', '')}.\n"
        return text
    
    def _format_guardianship_clause(self, data):
        if data.get('minor_children', False) and data.get('guardian_name'):
            return f"""Should any of my children be minors at the time of my death, I nominate {data.get('guardian_name', '')} of {data.get('guardian_address', '')} as guardian of the person and property of such minor children. 

In the event that {data.get('guardian_name', '')} is unable or unwilling to serve, I nominate {data.get('alternate_guardian', '[ALTERNATE GUARDIARIAN]')} as alternate guardian."""
        return "This clause does not apply as I have no minor children."

    def create_pdf_will(self, will_text, filename="will_document.pdf"):
        """Convert will text to PDF"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Split text into lines and add to PDF
            lines = will_text.split('\n')
            for line in lines:
                # Handle long lines
                if len(line) > 90:
                    words = line.split(' ')
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 90:
                            current_line += word + " "
                        else:
                            pdf.cell(0, 6, current_line.strip(), ln=True)
                            current_line = word + " "
                    if current_line:
                        pdf.cell(0, 6, current_line.strip(), ln=True)
                else:
                    pdf.cell(0, 6, line, ln=True)
            
            # Save PDF
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(temp_file.name)
            return temp_file.name
        except Exception as e:
            st.error(f"Error creating PDF: {str(e)}")
            return None

# ---------------- Styling ----------------
def apply_will_generator_styling():
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
    
    .will-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(37, 99, 235, 0.2);
    }
    
    .will-header h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .will-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        color: white !important;
    }
    
    /* Section cards */
    .section-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 1.5rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(59, 130, 246, 0.2) !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .section-card h2 {
        color: #1E40AF !important;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    
    /* Legal notice */
    .legal-notice {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05)) !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 6px solid #1D4ED8;
        color: #1E293B !important;
    }
    
    .legal-notice h3, .legal-notice p, .legal-notice li {
        color: #1E293B !important;
    }
    
    /* Buttons */
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
        margin: 1rem 0 !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1E40AF 0%, #7C3AED 50%, #EC4899 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Will preview */
    .will-preview {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(59, 130, 246, 0.2) !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .will-preview h3 {
        color: #1E40AF !important;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    /* Form elements */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox select {
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        color: #1E293B !important;
        background-color: rgba(255,255,255,0.9) !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(34, 197, 94, 0.05)) !important;
        padding: 1.5rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(34, 197, 94, 0.2) !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .success-box h3 {
        color: #166534 !important;
        margin-bottom: 0.5rem;
    }
    
    .success-box p {
        color: #166534 !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .will-header h1 {
            font-size: 2rem;
        }
        
        .section-card {
            padding: 1rem;
        }
        
        .main .block-container {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Helper Functions ----------------
def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate a download link for a binary file"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}" style="display: inline-block; text-align: center; text-decoration: none;"><div class="stButton"><button>Download {file_label}</button></div></a>'
    return href

# ---------------- Audio Guidance ----------------
def create_will_audio_guide(section, language='en'):
    """Create audio guidance for will sections"""
    guides = {
        'intro': "Welcome to the Will Generator. This tool will help you create a basic will document. Please note that while this generates a legal framework, you should consult with an attorney for complex estates or specific legal requirements.",
        'personal_info': "Please provide your full legal name and current address. This information will identify you as the testator in your will.",
        'beneficiaries': "Choose who will inherit your assets. Consider naming alternate beneficiaries in case your primary choice cannot inherit.",
        'executor': "Select a trustworthy person to carry out your will's instructions. This should be someone organized and responsible.",
        'witnesses': "Your will must be signed by at least two witnesses who are not beneficiaries. They confirm you signed the will voluntarily.",
        'completion': "Your will has been generated. Remember to sign it in front of witnesses and consider having it notarized for additional validity."
    }
    
    try:
        text = guides.get(section, "Section guidance not available.")
        tts = gTTS(text=text, lang=language, slow=False)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except:
        return None

# ---------------- Main Application ----------------
def run():
    apply_will_generator_styling()
    
    # Header with gradient text
    st.markdown(""" 
    <h1> ⚖️ Will Generator Tool</h1>
    <p style="text-align: center; font-size: 1.2rem; color: #64748B; margin-bottom: 2rem;">
        Create a legally sound will document to protect your assets and provide for your loved ones
    </p>
    """, unsafe_allow_html=True)
    
    # Legal notice
    st.markdown("""
    <div class="legal-notice">
        <h3>Legal Notice</h3>
        <p>This tool provides a basic will template. For complex estates, multiple properties, or specific legal requirements, 
        we strongly recommend consulting with a qualified legal professional. This document should be signed in the presence 
        of two competent witnesses who are not beneficiaries.</p>
    </div>
    """, unsafe_allow_html=True)

    if "will_data" not in st.session_state:
        st.session_state.will_data = {}

    # Step 1: Personal Details
    st.markdown("""
    <div class="section-card">
        <h2>Step 1: Personal Details</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.will_data['full_name'] = st.text_input(
            "Full Legal Name", 
            value=st.session_state.will_data.get('full_name', ''), 
            key="full_name",
            help="Enter your complete legal name as it appears on official documents"
        )
    with col2:
        st.session_state.will_data['id_number'] = st.text_input(
            "South African ID Number", 
            value=st.session_state.will_data.get('id_number', ''), 
            key="id_number",
            help="13-digit South African identity number"
        )
    
    st.session_state.will_data['address'] = st.text_area(
        "Current Residential Address", 
        value=st.session_state.will_data.get('address', ''), 
        key="address",
        height=80,
        help="Full physical address including city and postal code"
    )

    # Step 2: Beneficiaries
    st.markdown("""
    <div class="section-card">
        <h2>Step 2: Beneficiary Information</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.session_state.will_data['primary_beneficiary'] = st.text_input(
            "Primary Beneficiary Full Name", 
            value=st.session_state.will_data.get('primary_beneficiary', ''), 
            key="primary_beneficiary",
            help="Person who will inherit your estate"
        )
    with col2:
        st.session_state.will_data['beneficiary_relationship'] = st.text_input(
            "Relationship to Beneficiary", 
            value=st.session_state.will_data.get('beneficiary_relationship', ''), 
            key="beneficiary_relationship",
            help="e.g., Spouse, Child, Sibling, Friend"
        )
    with col3:
        st.session_state.will_data['beneficiary_share'] = st.number_input(
            "Estate Percentage", 
            min_value=0, 
            max_value=100, 
            value=st.session_state.will_data.get('beneficiary_share', 100), 
            key="beneficiary_share",
            help="Percentage of estate to inherit"
        )

    st.session_state.will_data['alternate_beneficiary'] = st.text_input(
        "Alternate Beneficiary", 
        value=st.session_state.will_data.get('alternate_beneficiary', ''), 
        key="alternate_beneficiary",
        help="Who should inherit if your primary beneficiary cannot"
    )

    # Step 3: Executor
    st.markdown("""
    <div class="section-card">
        <h2>Step 3: Executor Appointment</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.will_data['executor_name'] = st.text_input(
            "Executor Full Name", 
            value=st.session_state.will_data.get('executor_name', ''), 
            key="executor_name",
            help="Person responsible for administering your estate"
        )
    with col2:
        st.session_state.will_data['executor_address'] = st.text_input(
            "Executor Address", 
            value=st.session_state.will_data.get('executor_address', ''), 
            key="executor_address",
            help="Executor's full address"
        )

    st.session_state.will_data['alternate_executor'] = st.text_input(
        "Alternate Executor", 
        value=st.session_state.will_data.get('alternate_executor', ''), 
        key="alternate_executor",
        help="Who should serve as executor if your first choice cannot"
    )

    # Step 4: Guardian (Optional)
    st.markdown("""
    <div class="section-card">
        <h2>Step 4: Guardian Appointment (Optional)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.will_data['minor_children'] = st.checkbox(
        "I have minor children who would need a guardian",
        value=st.session_state.will_data.get('minor_children', False),
        key="minor_children"
    )
    
    if st.session_state.will_data.get('minor_children', False):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.will_data['guardian_name'] = st.text_input(
                "Guardian Full Name", 
                value=st.session_state.will_data.get('guardian_name', ''), 
                key="guardian_name",
                help="Guardian for minor children"
            )
        with col2:
            st.session_state.will_data['guardian_address'] = st.text_input(
                "Guardian Address", 
                value=st.session_state.will_data.get('guardian_address', ''), 
                key="guardian_address",
                help="Guardian's full address"
            )

        st.session_state.will_data['alternate_guardian'] = st.text_input(
            "Alternate Guardian", 
            value=st.session_state.will_data.get('alternate_guardian', ''), 
            key="alternate_guardian",
            help="Alternate guardian if your first choice cannot serve"
        )

    # Step 5: Witnesses
    st.markdown("""
    <div class="section-card">
        <h2>Step 5: Witness Information</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.will_data['witness1_name'] = st.text_input(
            "Witness 1 Full Name", 
            value=st.session_state.will_data.get('witness1_name', ''), 
            key="witness1_name",
            help="First witness (cannot be a beneficiary)"
        )
        st.session_state.will_data['witness1_address'] = st.text_input(
            "Witness 1 Address", 
            value=st.session_state.will_data.get('witness1_address', ''), 
            key="witness1_address",
            help="Witness 1's full address"
        )
    with col2:
        st.session_state.will_data['witness2_name'] = st.text_input(
            "Witness 2 Full Name", 
            value=st.session_state.will_data.get('witness2_name', ''), 
            key="witness2_name",
            help="Second witness (cannot be a beneficiary)"
        )
        st.session_state.will_data['witness2_address'] = st.text_input(
            "Witness 2 Address", 
            value=st.session_state.will_data.get('witness2_address', ''), 
            key="witness2_address",
            help="Witness 2's full address"
        )

    # Specific bequests
    st.markdown("""
    <div class="section-card">
        <h2>Specific Bequests (Optional)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("List specific items you want to leave to specific people")
    
    if "specific_bequests" not in st.session_state:
        st.session_state.specific_bequests = []
    
    with st.expander("Add Specific Bequest"):
        col1, col2 = st.columns(2)
        with col1:
            item = st.text_input("Item to Bequeath", key="bequest_item")
        with col2:
            beneficiary = st.text_input("Beneficiary Name", key="bequest_beneficiary")
        
        if st.button("Add Bequest", key="add_bequest"):
            if item and beneficiary:
                st.session_state.specific_bequests.append({
                    "item": item,
                    "beneficiary": beneficiary
                })
                st.success("Bequest added!")
                st.rerun()
    
    if st.session_state.specific_bequests:
        st.markdown("**Current Bequests:**")
        for i, bequest in enumerate(st.session_state.specific_bequests):
            st.markdown(f"{i+1}. {bequest['item']} → {bequest['beneficiary']}")
            if st.button(f"Remove #{i+1}", key=f"remove_{i}"):
                st.session_state.specific_bequests.pop(i)
                st.rerun()

    # Generate Will Button
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
    """, unsafe_allow_html=True)
    
    if st.button("Generate Will Document", key="generate_will", help="Create your will document based on the provided information"):
        # Validation
        required_fields = ['full_name', 'address', 'primary_beneficiary', 'executor_name']
        missing_fields = [field for field in required_fields if not st.session_state.will_data.get(field)]
        
        if missing_fields:
            st.error(f"Please complete the following required fields: {', '.join(missing_fields)}")
        else:
            st.subheader("Generated Will Document")
            
            will_generator = WillGenerator()
            st.session_state.will_data['specific_bequests'] = st.session_state.specific_bequests
            will_text = will_generator.create_simple_will_template(st.session_state.will_data)
            
            st.markdown("""
            <div class="will-preview">
                <h3>Will Document Preview</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_area("Generated Will Content", will_text, height=400, key="will_preview")
            
            # Download options
            st.markdown("""
            <div class="success-box">
                <h3>✅ Will Generation Complete</h3>
                <p>Your will document has been successfully generated. Please review it carefully and download using the buttons below.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download as PDF
                pdf_file = will_generator.create_pdf_will(will_text)
                if pdf_file:
                    st.markdown(get_binary_file_downloader_html(pdf_file, "PDF Will"), unsafe_allow_html=True)
            
            with col2:
                # Download as text
                text_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8')
                text_file.write(will_text)
                text_file.close()
                st.markdown(get_binary_file_downloader_html(text_file.name, "Text Will"), unsafe_allow_html=True)
            
            # Important instructions
            st.markdown("""
            <div class="legal-notice">
                <h3>Next Steps</h3>
                <ol>
                    <li>Print your will document</li>
                    <li>Sign it in the presence of two competent witnesses (who are not beneficiaries)</li>
                    <li>Have your witnesses sign in your presence and in each other's presence</li>
                    <li>Consider having the document notarized for additional legal validity</li>
                    <li>Store the original in a safe place and inform your executor of its location</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    run()