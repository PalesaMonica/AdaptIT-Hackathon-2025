# pages/ai_assistance.py
import streamlit as st
import numpy as np
import os, csv
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
import io
import tempfile
from gtts import gTTS

# ---------------- Config ----------------
DATA_FILE = "data/sassa_applications.csv"
HOME_VISITS_FILE = "data/home_visits.csv"
MAX_IMAGE_SIZE = 10*1024*1024
SUPPORTED_FORMATS = ["jpg","jpeg","png","webp"]
os.makedirs("data", exist_ok=True)

# ---------------- SASSA Colors & Styling ----------------
def apply_sassa_styling():
    st.markdown("""
    <style>
    /* SASSA Official Colors */
    :root {
        --sassa-green: #2E8B57;
        --sassa-gold: #FFD700;
        --sassa-dark-green: #1F5F3F;
        --sassa-light-green: #90EE90;
        --sassa-white: #FFFFFF;
    }
    
    /* Main background */
    .main .block-container {
        padding: 2rem;
        background: linear-gradient(135deg, #2E8B57 0%, #1F5F3F 100%);
        border-radius: 10px;
    }
    
    /* Title styling */
    .main h1 {
        color: #FFD700 !important;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
    }
    
    /* Section headers */
    .main h3 {
        color: #FFD700 !important;
        background: rgba(255, 215, 0, 0.1);
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #FFD700;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #FFFFFF !important;
        border: 2px solid #2E8B57 !important;
        border-radius: 5px !important;
        color: #1F5F3F !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        color: #1F5F3F !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #FFA500, #FFD700) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Progress bar */
    .stProgress .st-bo {
        background-color: #FFD700 !important;
    }
    
    /* File uploader */
    .stFileUploader label {
        color: #FFD700 !important;
        font-weight: bold !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(144, 238, 144, 0.2) !important;
        border: 1px solid #90EE90 !important;
        color: #1F5F3F !important;
    }
    
    .stError {
        background-color: rgba(255, 99, 71, 0.2) !important;
        border: 1px solid #FF6347 !important;
        color: #8B0000 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1F5F3F 0%, #2E8B57 100%);
    }
    
    /* Divider */
    hr {
        border-color: #FFD700 !important;
        opacity: 0.5;
    }
    
    /* Home visit info box */
    .home-visit-info {
        background: rgba(255, 215, 0, 0.1) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        color: #FFD700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- OCR ----------------
@st.cache_resource
def load_ocr_model():
    try:
        import easyocr
        return easyocr.Reader(['en','af'], gpu=False)  # English/Afrikaans supported
    except:
        st.error("Faka i-EasyOCR: pip install easyocr")
        return None

def preprocess_image(image):
    if image.mode != 'RGB': image = image.convert('RGB')
    image = ImageEnhance.Contrast(image).enhance(1.5)
    image = ImageEnhance.Sharpness(image).enhance(1.3)
    image = image.convert('L')
    image = image.filter(ImageFilter.MedianFilter(size=3))
    return image

def extract_text_from_image(image, ocr_reader):
    processed = preprocess_image(image)
    arr = np.array(processed)
    try:
        return ' '.join(ocr_reader.readtext(arr, detail=0, paragraph=True)).strip()
    except:
        return ""

# ---------------- CSV ----------------
def initialize_csv():
    if not os.path.exists(DATA_FILE):
        fields = ["timestamp","igama_eliphelele","inombolo_ye_id","uhlobo_lwesibonelelo","inombolo_yefoni",
                  "ikheli","imali_yenyanga","amalungu_asekhaya","ulwazi_lokukhubazeka",
                  "amanye_amanothi","imithombo_yezithombe","home_visit_requested","mobility_details"]
        with open(DATA_FILE,"w",newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

    # Initialize home visits CSV
    if not os.path.exists(HOME_VISITS_FILE):
        fields = ["timestamp","full_name","id_number","phone_number","address","service_type",
                  "mobility_reason","preferred_time","special_requirements","status","agent_assigned"]
        with open(HOME_VISITS_FILE,"w",newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

# ---------------- Audio Guidance ----------------
def play_audio_instruction(text_zu, text_en):
    col1, col2 = st.columns(2)
    with col1:
        try:
            tts_zu = gTTS(text=text_zu, lang='zu')
            tmp_file_zu = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts_zu.save(tmp_file_zu.name)
            st.audio(tmp_file_zu.name, format="audio/mp3")
            st.caption("🔊 isiZulu")
        except:
            st.caption("Umsindo awutholakali - Audio unavailable")
    
    with col2:
        try:
            tts_en = gTTS(text=text_en, lang='en')
            tmp_file_en = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts_en.save(tmp_file_en.name)
            st.audio(tmp_file_en.name, format="audio/mp3")
            st.caption("🔊 English")
        except:
            st.caption("Audio unavailable")

# ---------------- Home Visit Functions ----------------
def show_home_visit_option():
    st.markdown("""
    <div class="home-visit-info">
    <h4>🏠 Ukuvakashela Ekhaya / Home Visit Service</h4>
    <p>Uma ungezikhundla zokuvakashela ihhovisi: / If you cannot visit an office:</p>
    <ul>
    <li>Abantu abadala (65+) / Elderly persons (65+)</li>
    <li>Abantu abakhubazekile / People with disabilities</li>
    <li>Izindawo ezikude / Remote locations</li>
    <li>Amakhono okuhamba / Mobility challenges</li>
    </ul>
    <p><strong>Iqembu lethu liya ekuyadleni / Our team comes to you!</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.checkbox(
        "🏠 Ngicela ukuvakashela ekhaya / I request a home visit",
        help="Khomba uma ungakwazi ukuya ehhovisi ngenxa yobudala, ukukhubazeka, noma ukude / Check if you cannot visit office due to age, disability, or distance"
    )

def home_visit_details_form():
    st.markdown("### 🏠 Imininingwane Yokuvakashela Ekhaya / Home Visit Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        mobility_reason = st.selectbox(
            "Isizathu sokucela ukuvakashela ekhaya / Reason for home visit request:",
            [
                "Ubudala (65+) / Advanced age (65+)",
                "Ukukhubazeka okumubambekile / Physical disability", 
                "Ukugula okudingeka ukunakekelwa / Serious illness requiring care",
                "Indawo ekude / Remote location",
                "Akukho ukuthutha / No transportation",
                "Abanye ababangela / Other reasons"
            ]
        )
        
        preferred_time = st.selectbox(
            "Isikhathi osiskhethayo / Preferred time:",
            [
                "Ekuseni (08:00-12:00) / Morning (08:00-12:00)",
                "Emini (12:00-15:00) / Afternoon (12:00-15:00)", 
                "Ntambama (15:00-17:00) / Late afternoon (15:00-17:00)",
                "Noma nini / Any time"
            ]
        )
    
    with col2:
        special_requirements = st.text_area(
            "Izidingo ezikhethekile / Special requirements:",
            placeholder="Izibonelo: Isiguli esisebenzisa iwheelchair, udinga umtoliki, nezinye izidingo ezifanele / Examples: Wheelchair access needed, interpreter required, other special needs",
            help="Chaza noma yiziphi izidingo ezikhethekile ezingasiza umhlanganisi wethu / Describe any special needs that can help our agent"
        )
        
        emergency_contact = st.text_input(
            "Umuntu wokuthintana nezimo eziphuthumayo / Emergency contact:",
            placeholder="Igama nonombolo / Name and number",
            help="Umuntu ozokuthintana naye uma siludinga / Person to contact if needed"
        )
    
    # Audio instructions for home visit
    st.markdown("#### 🔊 Izixwayiso zomsindo / Audio Instructions")
    play_audio_instruction(
        "Umhlanganisi wethu uzofika ekhaya lakho ngesikhathi esivumelekile. Qiniseka ukuba unezincwadi ezidingekayo futhi umuntu omdala ukhona.",
        "Our agent will visit your home at the agreed time. Please ensure you have required documents and an adult is present."
    )
    
    return mobility_reason, preferred_time, special_requirements, emergency_contact

def save_home_visit_request(form_data, visit_data):
    """Save home visit request to separate CSV file"""
    home_visit_record = {
        "timestamp": datetime.now().isoformat(),
        "full_name": form_data.get('igama_eliphelele', ''),
        "id_number": form_data.get('inombolo_ye_id', ''),
        "phone_number": form_data.get('inombolo_yefoni', ''),
        "address": form_data.get('ikheli', ''),
        "service_type": form_data.get('uhlobo_lwesibonelelo', ''),
        "mobility_reason": visit_data[0],
        "preferred_time": visit_data[1], 
        "special_requirements": visit_data[2],
        "emergency_contact": visit_data[3],
        "status": "Pending Assignment",
        "agent_assigned": ""
    }
    
    with open(HOME_VISITS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(home_visit_record.keys()))
        writer.writerow(home_visit_record)

# ---------------- Field Step ----------------
def field_step(field_name, icon, ocr_reader, instruction_zu, instruction_en, display_name, options=None):
    st.markdown(f"### {icon} {display_name}")
    play_audio_instruction(instruction_zu, instruction_en)

    col1, col2 = st.columns([1,2])
    text_value = ""
    uploaded_file = None
    
    with col1:
        uploaded_file = st.file_uploader(
            f"Layisha isithombe se-{display_name} / Upload image for {display_name.lower()}", 
            type=SUPPORTED_FORMATS, 
            key=f"file_{field_name}"
        )
        if uploaded_file:
            if uploaded_file.size > MAX_IMAGE_SIZE:
                st.error(f"Isithombe sikhulu kakhulu (max 10MB) / Image too large (max 10MB)")
            else:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"{display_name} preview")
                text_value = extract_text_from_image(image, ocr_reader)
    
    with col2:
        if options:
            # Grant type selectbox
            current = options.index(text_value) if text_value in options else 0
            text_value = st.selectbox(f"{display_name}", options=options, index=current, key=f"text_{field_name}")
        else:
            text_value = st.text_input(f"{display_name}", value=text_value, key=f"text_{field_name}")

    return text_value, uploaded_file.name if uploaded_file else ""

# ---------------- Main App ----------------
def run():
    st.set_page_config(
        page_title="I-SASSA Visual Form", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    apply_sassa_styling()
    initialize_csv()
    ocr_reader = load_ocr_model()

    st.title("🇿🇦 I-SASSA Visual Form")
    st.markdown("**Landela izinyathelo ngezithombe nezixwayiso zomsindo / Follow the steps with pictures and audio prompts**")

    # Show home visit option at the top
    home_visit_requested = show_home_visit_option()

    # Define fields with isiZulu translations
    field_info = {
        "igama_eliphelele": (
            "👤", 
            "Sicela ulayishe noma ubhale igama lakho eliphelele njengoba libonakala ku-ID yakho.",
            "Please upload or type your full name as it appears on your ID.",
            "Igama Eliphelele / Full Name"
        ),
        "inombolo_ye_id": (
            "🆔", 
            "Sicela ulayishe noma ubhale inombolo yakho ye-ID yaseNingizimu Afrika enezinombolo ezingu-13.",
            "Please upload or type your 13-digit South African ID number.",
            "Inombolo ye-ID / ID Number"
        ),
        "ikheli": (
            "🏠", 
            "Sicela ulayishe noma ubhale ikheli lakho lokuhlala okwamanje.",
            "Please upload or type your current residential address.",
            "Ikheli / Address"
        ),
        "inombolo_yefoni": (
            "📱", 
            "Sicela ulayishe noma ubhale inombolo yakho yeselula.",
            "Please upload or type your cellphone number.",
            "Inombolo Yefoni / Phone Number"
        ),
        "imali_yenyanga": (
            "💵", 
            "Sicela ulayishe noma ubhale imali yakho yonke yenyanga.",
            "Please upload or type your total monthly income.",
            "Imali Yenyanga / Monthly Income"
        ),
        "amalungu_asekhaya": (
            "👥", 
            "Sicela ulayishe noma ubhale inombolo yabantu abahlala ekhaya lakho.",
            "Please upload or type the number of people living in your household.",
            "Amalungu Asekhaya / Household Members"
        ),
        "uhlobo_lwesibonelelo": (
            "💰", 
            "Sicela ukhethe uhlobo lwesibonelelo osicela sona.",
            "Please select the type of grant you are applying for.",
            "Uhlobo Lwesibonelelo / Grant Type"
        ),
        "ulwazi_lokukhubazeka": (
            "🏥", 
            "Sicela ulayishe noma ubhale noma yiluphi ulwazi oluhlobene nezempilo noma ukukhubazeka.",
            "Please upload or type any relevant medical or disability information.",
            "Ulwazi Lokukhubazeka / Disability Information"
        )
    }

    # Grant options in isiZulu and English
    grant_options = [
        "Ipensheni Yobudala / Old Age Pension",
        "Isibonelelo Sokusekela Ingane / Child Support Grant", 
        "Isibonelelo Sokukhubazeka / Disability Grant",
        "Isibonelelo Sengane Esinakekelwayo / Foster Child Grant",
        "Isibonelelo Lokunakekela / Care Dependency Grant"
    ]

    field_data = {}
    image_sources = []

    for field, (icon, audio_zu, audio_en, display_name) in field_info.items():
        if field == "uhlobo_lwesibonelelo":
            val, img_name = field_step(field, icon, ocr_reader, audio_zu, audio_en, display_name, options=grant_options)
        else:
            val, img_name = field_step(field, icon, ocr_reader, audio_zu, audio_en, display_name)
        field_data[field] = val
        if img_name: image_sources.append(f"{field}: {img_name}")
        st.markdown("---")

    # Home visit details if requested
    visit_data = None
    if home_visit_requested:
        visit_data = home_visit_details_form()
        st.markdown("---")

    # Additional Notes
    field_data['amanye_amanothi'] = st.text_area(
        "📝 Amanye Amanothi (Ongakukhetha) / Additional Notes (Optional)",
        help="Bhala noma yini oyifuna ukuyengeza / Write anything you want to add"
    )

    # Progress bar with bilingual label
    completed = sum(1 for f in field_data if field_data[f])
    total = len(field_data)-1  # exclude additional notes
    progress_value = min(completed/total, 1.0)
    st.markdown(f"**Inqubekelaphambili / Progress: {int(progress_value*100)}%**")
    st.progress(progress_value)

    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_text = "🏠 Thumela Isicelo Lokuvakashela Ekhaya / Submit Home Visit Request" if home_visit_requested else "📤 Thumela Isicelo / Submit Application"
        
        if st.button(submit_text, key="submit"):
            errors = []
            if not field_data['igama_eliphelele']: 
                errors.append("Igama eliphelele liyadingeka / Full Name required")
            if not field_data['inombolo_ye_id']: 
                errors.append("Inombolo ye-ID iyadingeka / ID Number required")
            if not field_data['inombolo_yefoni']:
                errors.append("Inombolo Yefoni iyasingeka / Phone Number required")
            if not field_data['ikheli']:
                errors.append("Ikheli iyasingeka / Address required")
            if not field_data['uhlobo_lwesibonelelo']: 
                errors.append("Uhlobo lwesibonelelo luyadingeka / Grant Type required")
            
            if errors:
                for e in errors: 
                    st.error(f"⚠️ {e}")
            else:
                # Convert field names back to English for CSV compatibility
                english_mapping = {
                    'igama_eliphelele': 'full_name',
                    'inombolo_ye_id': 'id_number', 
                    'uhlobo_lwesibonelelo': 'grant_type',
                    'inombolo_yefoni': 'phone_number',
                    'ikheli': 'address',
                    'imali_yenyanga': 'monthly_income',
                    'amalungu_asekhaya': 'household_members',
                    'ulwazi_lokukhubazeka': 'disability_info',
                    'amanye_amanothi': 'additional_notes'
                }
                
                app_data = {}
                for zu_field, en_field in english_mapping.items():
                    app_data[en_field] = field_data.get(zu_field, '')
                
                app_data.update({
                    "timestamp": datetime.now().isoformat(),
                    "image_sources": ', '.join(image_sources),
                    "home_visit_requested": "Yes" if home_visit_requested else "No",
                    "mobility_details": visit_data[0] if visit_data else ""
                })
                
                # Save main application
                csv_file = "data/sassa_applications.csv"
                if not os.path.exists(csv_file):
                    with open(csv_file, "w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=list(app_data.keys()))
                        writer.writeheader()
                
                with open(csv_file, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=list(app_data.keys()))
                    writer.writerow(app_data)
                
                # Save home visit request if applicable
                if home_visit_requested and visit_data:
                    save_home_visit_request(field_data, visit_data)
                
                if app_data:
                    if home_visit_requested:
                        st.success("""
                        ✅ Isicelo sokuvakashela ekhaya sithunyelwe ngempumelelo! 
                        
                        🏠 Home visit request submitted successfully!
                        
                        📞 Umhlanganisi wethu uzokuthinta maduze ukuze ahlele ukuvakashela
                        
                        📞 Our agent will contact you soon to arrange the visit
                        
                        📋 Lungisa izincwadi ezidingekayo / Prepare required documents
                        """)
                    else:
                        st.success("Isicelo sithunyelwe ngempumelelo! / Application submitted successfully!")