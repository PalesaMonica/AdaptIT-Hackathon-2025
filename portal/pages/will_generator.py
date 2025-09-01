import streamlit as st
import datetime
from fpdf import FPDF
import tempfile
import os
from gtts import gTTS

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

In the event that {data.get('guardian_name', '')} is unable or unwilling to serve, I nominate {data.get('alternate_guardian', '[ALTERNATE GUARDIAN]')} as alternate guardian."""
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
    .main .block-container {
        padding: 2rem;
        max-width: 1000px;
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
    }
    
    .section-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .section-card h2 {
        color: #1E3A8A !important;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    
    .legal-notice {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 6px solid #1D4ED8;
    }
    
    .generate-button {
        background: linear-gradient(45deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: white !important;
        font-weight: bold;
        font-size: 1.2rem;
        padding: 1rem 2rem;
        border: none !important;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 100%;
        margin: 1rem 0;
    }
    
    .generate-button:hover {
        background: linear-gradient(45deg, #1E40AF 0%, #2563EB 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
    }
    
    .will-preview {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 2px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .will-preview h3 {
        color: #1E3A8A !important;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .stTextArea textarea {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    @media (max-width: 768px) {
        .will-header h1 {
            font-size: 2rem;
        }
        
        .section-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

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
    
    # Header
    st.markdown("""
    <div class="will-header">
        <h1>Will Generator Tool</h1>
        <p>Create a legally sound will document to protect your assets and provide for your loved ones</p>
        <p><small>Professional will drafting with comprehensive legal framework</small></p>
    </div>
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
        st.session_state.will_data['beneficiary_name'] = st.text_input(
            "Primary Beneficiary Full Name", 
            value=st.session_state.will_data.get('beneficiary_name', ''), 
            key="beneficiary_name",
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

    # Step 3: Executor
    st.markdown("""
    <div class="section-card">
        <h2>Step 3: Executor Appointment</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.session_state.will_data['executor_name'] = st.text_input(
            "Executor Full Name", 
            value=st.session_state.will_data.get('executor_name', ''), 
            key="executor_name",
            help="Person responsible for administering your estate"
        )
    with col2:
        st.session_state.will_data['executor_relationship'] = st.text_input(
            "Executor Relationship", 
            value=st.session_state.will_data.get('executor_relationship', ''), 
            key="executor_relationship",
            help="Relationship to executor"
        )
    with col3:
        st.session_state.will_data['executor_phone'] = st.text_input(
            "Executor Phone", 
            value=st.session_state.will_data.get('executor_phone', ''), 
            key="executor_phone",
            help="Contact number for executor"
        )

    # Step 4: Guardian (Optional)
    st.markdown("""
    <div class="section-card">
        <h2>Step 4: Guardian Appointment (Optional)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.session_state.will_data['guardian_name'] = st.text_input(
            "Guardian Full Name", 
            value=st.session_state.will_data.get('guardian_name', ''), 
            key="guardian_name",
            help="Guardian for minor children if applicable"
        )
    with col2:
        st.session_state.will_data['guardian_relationship'] = st.text_input(
            "Guardian Relationship", 
            value=st.session_state.will_data.get('guardian_relationship', ''), 
            key="guardian_relationship",
            help="Relationship to guardian"
        )
    with col3:
        st.session_state.will_data['guardian_phone'] = st.text_input(
            "Guardian Phone", 
            value=st.session_state.will_data.get('guardian_phone', ''), 
            key="guardian_phone",
            help="Contact number for guardian"
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
        st.session_state.will_data['witness1_phone'] = st.text_input(
            "Witness 1 Phone", 
            value=st.session_state.will_data.get('witness1_phone', ''), 
            key="witness1_phone",
            help="Contact number for witness 1"
        )
    with col2:
        st.session_state.will_data['witness2_name'] = st.text_input(
            "Witness 2 Full Name", 
            value=st.session_state.will_data.get('witness2_name', ''), 
            key="witness2_name",
            help="Second witness (cannot be a beneficiary)"
        )
        st.session_state.will_data['witness2_phone'] = st.text_input(
            "Witness 2 Phone", 
            value=st.session_state.will_data.get('witness2_phone', ''), 
            key="witness2_phone",
            help="Contact number for witness 2"
        )

    # Generate Will Button
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
    """, unsafe_allow_html=True)
    
    if st.button("Generate Will Document", key="generate_will", help="Create your will document based on the provided information"):
        # Validation
        required_fields = ['full_name', 'address', 'beneficiary_name', 'executor_name']
        missing_fields = [field for field in required_fields if not st.session_state.will_data.get(field)]
        
        if missing_fields:
            st.error(f"Please complete the following required fields: {', '.join(missing_fields)}")
        else:
            st.subheader("Generated Will Document")
            
            will_text = f"""
LAST WILL AND TESTAMENT

I, {st.session_state.will_data.get('full_name')}, ID Number {st.session_state.will_data.get('id_number', '')}, 
residing at {st.session_state.will_data.get('address')}, hereby declare this to be my Last Will and Testament.

ARTICLE I - PERSONAL DETAILS
I declare that I am of sound mind and disposing memory, and I make this Will voluntarily.

ARTICLE II - BENEFICIARIES
I give, devise and bequeath my entire estate to {st.session_state.will_data.get('beneficiary_name')} 
({st.session_state.will_data.get('beneficiary_relationship')}), who shall inherit {st.session_state.will_data.get('beneficiary_share')}% of my estate.

ARTICLE III - EXECUTOR
I appoint {st.session_state.will_data.get('executor_name')} ({st.session_state.will_data.get('executor_relationship')}) 
as the Executor of this Will. Contact: {st.session_state.will_data.get('executor_phone', '')}.

ARTICLE IV - GUARDIANSHIP
{('I appoint ' + st.session_state.will_data.get('guardian_name') + ' (' + st.session_state.will_data.get('guardian_relationship') + ') as guardian of any minor children. Contact: ' + st.session_state.will_data.get('guardian_phone', '') + '.') if st.session_state.will_data.get('guardian_name') else 'No guardian appointment specified.'}

ARTICLE V - WITNESSES
This Will shall be signed in the presence of:
1. {st.session_state.will_data.get('witness1_name', '')} (Contact: {st.session_state.will_data.get('witness1_phone', '')})
2. {st.session_state.will_data.get('witness2_name', '')} (Contact: {st.session_state.will_data.get('witness2_phone', '')})

IN WITNESS WHEREOF, I set my hand this {datetime.date.today().strftime('%d day of %B, %Y')}.

_________________________________
{st.session_state.will_data.get('full_name')}
Testator

WITNESSED BY:

1. _________________________________
{st.session_state.will_data.get('witness1_name', '')}
Date: ____________________________

2. _________________________________
{st.session_state.will_data.get('witness2_name', '')}
Date: ____________________________
"""
            
            st.markdown("""
            <div class="will-preview">
                <h3>Will Document Preview</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_area("Generated Will Content", will_text, height=400, key="will_preview")
            
            # Download options
            st.info("Please review the document carefully. For legal validity, this document must be printed and signed in the presence of two competent witnesses.")

    st.markdown("</div>", unsafe_allow_html=True)