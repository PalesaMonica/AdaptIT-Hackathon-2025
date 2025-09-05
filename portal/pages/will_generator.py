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
            return f'<a href="data:application/octet-stream;base64,{b64}" download="Will.pdf" style="text-decoration: none; background: linear-gradient(to right, #4361ee, #7209b7); color: white; padding: 12px 24px; border-radius: 8px; font-weight: bold;">📥 Download Your Will</a>'
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

# --- run APP ---
def run():
    st.set_page_config(page_title="South African Will Generator", page_icon="✍️", layout="wide")

    # --- CUSTOM CSS ---
    st.markdown("""
    <style>
        :root {
            --primary: #4361ee;
            --secondary: #7209b7;
        }
        body {
            background: linear-gradient(135deg, #f7f9fc 0%, #eef2f7 100%);
            color: #333333;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background: linear-gradient(to right, var(--primary), var(--secondary));
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            background: linear-gradient(to right, #3a56d4, #6506a1);
            color: #ffffff;
        }
        .stProgress .st-bo {
            background: linear-gradient(to right, var(--primary), var(--secondary));
        }
        .title {
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 20px;
            padding: 10px;
        }
        .subtitle {
            font-size: 22px;
            font-weight: 700;
            color: var(--primary);
            margin-top: 10px;
            margin-bottom: 15px;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.08);
            margin-bottom: 25px;
            border-left: 5px solid var(--primary);
        }
        .awareness-card {
            background: linear-gradient(135deg, #f0f4ff 0%, #f8f0ff 100%);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid #e0e0ff;
        }
        .beneficiary-form {
            background: #f8f9ff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border: 1px solid #e0e5ff;
        }
        .section-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .section-number {
            background: linear-gradient(to right, var(--primary), var(--secondary));
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            font-weight: bold;
        }
        .info-point {
            display: flex;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        .info-icon {
            background: linear-gradient(to right, var(--primary), var(--secondary));
            color: white;
            min-width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

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
    st.markdown('<div class="title">✍️ South African Will Generator</div>', unsafe_allow_html=True)
    st.progress(st.session_state.step / 5)

    # --- STEP 1: Awareness ---
    if st.session_state.step == 1:
        st.markdown('<div class="section-header"><div class="section-number">1</div><div class="subtitle">Why You Need a Will</div></div>', unsafe_allow_html=True)
        
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
                "content": "It's not easy to think about — but making a will is an act of love and protection for your family."
            }
        ]
        
        for i, point in enumerate(awareness_points):
            st.markdown(f'''
            <div class="awareness-card">
                <div class="info-point">
                    <div class="info-icon">{i+1}</div>
                    <div>
                        <h4 style="margin: 0; color: var(--primary);">{point['title']}</h4>
                        <p style="margin: 5px 0 0 0;">{point['content']}</p>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Create My Will →", key="start_btn", use_container_width=True):
                st.session_state.step = 2
                st.rerun()

    # --- STEP 2: Assets ---
    elif st.session_state.step == 2:
        st.markdown('<div class="section-header"><div class="section-number">2</div><div class="subtitle">Select Your Assets</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
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
            if st.button("Continue →", key="assets_btn", use_container_width=True):
                st.session_state.form_data["assets"] = selected_assets
                st.session_state.step = 3
                st.rerun()

    # --- STEP 3: Beneficiaries ---
    elif st.session_state.step == 3:
        st.markdown('<div class="section-header"><div class="section-number">3</div><div class="subtitle">Add Beneficiaries</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
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
            
            add_beneficiary = st.form_submit_button("➕ Add Beneficiary")
            
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
                st.markdown(f"""
                <div class="beneficiary-form">
                    <b>{beneficiary['name']}</b> ({beneficiary['relationship']}) - To receive: {beneficiary['share']}
                    <button style="float: right; background: #ff4b4b; color: white; border: none; border-radius: 4px; padding: 2px 8px;" 
                            onclick="window.parent.postMessage({{'type': 'removeBeneficiary', 'index': {i}}}, '*');">
                        Remove
                    </button>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue →", key="beneficiaries_btn", use_container_width=True) and st.session_state.beneficiaries:
                st.session_state.form_data["beneficiaries"] = st.session_state.beneficiaries
                st.session_state.step = 4
                st.rerun()
            elif not st.session_state.beneficiaries:
                st.warning("Please add at least one beneficiary before continuing")

    # --- STEP 4: Executor ---
    elif st.session_state.step == 4:
        st.markdown('<div class="section-header"><div class="section-number">4</div><div class="subtitle">Appoint an Executor</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.info("The executor is responsible for carrying out the instructions in your will and managing your estate.")
        
        executor_name = st.text_input("Executor's Full Name")
        executor_contact = st.text_input("Executor's Contact Information")
        alternate_executor = st.text_input("Alternate Executor (optional)", 
                                         help="Someone to serve as executor if your first choice is unable to")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue →", key="executor_btn", use_container_width=True) and executor_name:
                st.session_state.form_data["executor"] = f"{executor_name} ({executor_contact})" if executor_contact else executor_name
                if alternate_executor:
                    st.session_state.form_data["executor"] += f" with {alternate_executor} as alternate"
                st.session_state.step = 5
                st.rerun()
            elif not executor_name:
                st.warning("Please appoint an executor before continuing")

    # --- STEP 5: Witnesses + Generate Will ---
    elif st.session_state.step == 5:
        st.markdown('<div class="section-header"><div class="section-number">5</div><div class="subtitle">Final Details</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
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
                    
                    st.success("""
                     Your will has been generated successfully! 
                    
                    **Next Steps:**
                    1. Download and print your will
                    2. Sign it in the presence of two competent witnesses
                    3. Have your witnesses sign in your presence and in each other's presence
                    4. Store it in a safe place and inform your executor of its location
                    """)
                    
                    st.markdown(download_pdf(pdf), unsafe_allow_html=True)
                    play_audio("Your will has been successfully generated. Please remember to print it and sign in front of two witnesses.")
                except Exception as e:
                    st.error(f"Error generating will: {str(e)}")
            elif not (name and address):
                st.warning("Please enter your name and address")
            elif len(witnesses) < 2:
                st.warning("Please provide at least two witnesses")

# JavaScript to handle beneficiary removal
st.components.v1.html("""
<script>
window.addEventListener('message', function(event) {
    if (event.data.type === 'removeBeneficiary') {
        // This is a placeholder - in a real implementation, you would need to
        // handle this with Streamlit's component system
        alert('Remove functionality would be implemented here');
    }
});
</script>
""", height=0)

