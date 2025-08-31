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
    :root {
        --will-blue: #1E40AF;
        --will-gold: #F59E0B;
        --will-green: #059669;
        --will-gray: #374151;
    }
    .main .block-container {
        padding: 2rem;
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
        border-radius: 10px;
        color: white;
    }
    .main h1 {
        color: #F59E0B !important;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .main h2, .main h3 {
        color: #F59E0B !important;
        border-left: 5px solid #F59E0B;
        padding-left: 10px;
    }
    .stButton > button {
        background: linear-gradient(45deg, #F59E0B, #FBBF24) !important;
        color: #1E40AF !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .will-section {
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #F59E0B;
    }
    .warning-box {
        background: linear-gradient(45deg, #DC2626, #EF4444);
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #B91C1C;
        margin: 20px 0;
    }
    .info-box {
        background: linear-gradient(45deg, #059669, #10B981);
        color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #047857;
        margin: 20px 0;
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
import streamlit as st

def run():
    st.title("📝 Will Generator Tool")

    if "will_data" not in st.session_state:
        st.session_state.will_data = {}

    # Step 1: Personal Details
    st.header("Step 1: Personal Details")
    st.session_state.will_data['full_name'] = st.text_input(
        "Full Name", 
        value=st.session_state.will_data.get('full_name', ''), 
        key="full_name"
    )
    st.session_state.will_data['id_number'] = st.text_input(
        "ID Number", 
        value=st.session_state.will_data.get('id_number', ''), 
        key="id_number"
    )
    st.session_state.will_data['address'] = st.text_area(
        "Address", 
        value=st.session_state.will_data.get('address', ''), 
        key="address"
    )

    # Step 2: Beneficiaries
    st.header("Step 2: Beneficiaries")
    st.session_state.will_data['beneficiary_name'] = st.text_input(
        "Beneficiary Full Name", 
        value=st.session_state.will_data.get('beneficiary_name', ''), 
        key="beneficiary_name"
    )
    st.session_state.will_data['beneficiary_relationship'] = st.text_input(
        "Relationship to you", 
        value=st.session_state.will_data.get('beneficiary_relationship', ''), 
        key="beneficiary_relationship"
    )
    st.session_state.will_data['beneficiary_share'] = st.number_input(
        "Percentage of Estate (%)", 
        min_value=0, 
        max_value=100, 
        value=st.session_state.will_data.get('beneficiary_share', 0), 
        key="beneficiary_share"
    )

    # Step 3: Executor
    st.header("Step 3: Executor Details")
    st.session_state.will_data['executor_name'] = st.text_input(
        "Executor Full Name", 
        value=st.session_state.will_data.get('executor_name', ''), 
        key="executor_name"
    )
    st.session_state.will_data['executor_relationship'] = st.text_input(
        "Relationship to you", 
        value=st.session_state.will_data.get('executor_relationship', ''), 
        key="executor_relationship"
    )
    st.session_state.will_data['executor_phone'] = st.text_input(
        "Phone Number", 
        value=st.session_state.will_data.get('executor_phone', ''), 
        key="executor_phone"
    )

    # Step 4: Guardian (Optional)
    st.header("Step 4: Guardian (Optional)")
    st.session_state.will_data['guardian_name'] = st.text_input(
        "Guardian Full Name", 
        value=st.session_state.will_data.get('guardian_name', ''), 
        key="guardian_name"
    )
    st.session_state.will_data['guardian_relationship'] = st.text_input(
        "Relationship to you", 
        value=st.session_state.will_data.get('guardian_relationship', ''), 
        key="guardian_relationship"
    )
    st.session_state.will_data['guardian_phone'] = st.text_input(
        "Phone Number", 
        value=st.session_state.will_data.get('guardian_phone', ''), 
        key="guardian_phone"
    )

    # Step 5: Witnesses
    st.header("Step 5: Witnesses")
    st.session_state.will_data['witness1_name'] = st.text_input(
        "Witness 1 Full Name", 
        value=st.session_state.will_data.get('witness1_name', ''), 
        key="witness1_name"
    )
    st.session_state.will_data['witness1_phone'] = st.text_input(
        "Witness 1 Phone", 
        value=st.session_state.will_data.get('witness1_phone', ''), 
        key="witness1_phone"
    )
    st.session_state.will_data['witness2_name'] = st.text_input(
        "Witness 2 Full Name", 
        value=st.session_state.will_data.get('witness2_name', ''), 
        key="witness2_name"
    )
    st.session_state.will_data['witness2_phone'] = st.text_input(
        "Witness 2 Phone", 
        value=st.session_state.will_data.get('witness2_phone', ''), 
        key="witness2_phone"
    )

    # Generate Will
    if st.button("Generate Will Document"):
        st.subheader("📄 Your Draft Will")
        will_text = f"""
        LAST WILL AND TESTAMENT

        I, {st.session_state.will_data.get('full_name')}, ID {st.session_state.will_data.get('id_number')}, 
        residing at {st.session_state.will_data.get('address')}, hereby declare this to be my Last Will.

        1. Beneficiaries:
           - {st.session_state.will_data.get('beneficiary_name')} 
             ({st.session_state.will_data.get('beneficiary_relationship')}), 
             shall inherit {st.session_state.will_data.get('beneficiary_share')}% of my estate.

        2. Executor:
           - {st.session_state.will_data.get('executor_name')} 
             ({st.session_state.will_data.get('executor_relationship')}), 
             Phone: {st.session_state.will_data.get('executor_phone')}, 
             is appointed as the executor of this Will.

        3. Guardian (if applicable):
           - {st.session_state.will_data.get('guardian_name')} 
             ({st.session_state.will_data.get('guardian_relationship')}), 
             Phone: {st.session_state.will_data.get('guardian_phone')}, 
             is appointed as guardian of my minor children.

        4. Witnesses:
           - {st.session_state.will_data.get('witness1_name')} (Phone: {st.session_state.will_data.get('witness1_phone')})
           - {st.session_state.will_data.get('witness2_name')} (Phone: {st.session_state.will_data.get('witness2_phone')})

        This Will is made freely, voluntarily, and in sound mind.
        """
        st.text_area("Generated Will", will_text, height=400)
