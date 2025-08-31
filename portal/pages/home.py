import streamlit as st
from gtts import gTTS
import tempfile

# ---------------- Legal Literacy Styling ----------------
def apply_legal_home_styling():
    st.markdown("""
    <style>
    /* Main background with legal justice colors */
    .main .block-container {
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #0B132B 0%, #1C2541 50%, #3A506B 100%);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Hero section styling */
    .hero-section {
        background: linear-gradient(45deg, rgba(255,215,0,0.15), rgba(255,255,255,0.05));
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        border: 2px solid rgba(255,215,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    .hero-title {
        color: #FFD700;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        color: #FFFFFF;
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
    }
    
    /* Service cards styling */
    .service-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.05));
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid rgba(255,215,0,0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    
    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(255,215,0,0.3);
        border-color: rgba(255,215,0,0.6);
    }
    
    .card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        text-align: center;
    }
    
    .card-title {
        color: #FFD700;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
    }
    
    .card-description {
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Override default Streamlit button styling */
    .stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        color: #0B132B !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #FFA500, #FFD700) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255,215,0,0.5) !important;
    }
    
    /* Stats section */
    .stats-section {
        background: rgba(255,215,0,0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 2rem 0;
        border-left: 5px solid #FFD700;
    }
    .stat-item {
        text-align: center;
        color: #FFFFFF;
        margin: 0.5rem 0;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #FFD700;
        display: block;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #CCCCCC;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Audio Guidance ----------------
def play_audio(text="Welcome to the Legal Literacy Portal!"):
    try:
        tts = gTTS(text=text, lang="en")
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        st.audio(tmp_file.name, format="audio/mp3")
    except:
        st.warning("🔇 Audio guidance unavailable")

# ---------------- Service Cards ----------------
def create_service_card(icon, title, description, button_text, page_key, audio_text):
    st.markdown(f"""
    <div class="service-card">
        <div class="card-icon">{icon}</div>
        <div class="card-title">{title}</div>
        <div class="card-description">{description}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(button_text, key=f"btn_{page_key}"):
        st.session_state['page'] = page_key
        try:
            tts = gTTS(text=audio_text, lang="en")
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp_file.name)
            st.audio(tmp_file.name, format="audio/mp3")
        except:
            pass

# ------------------ Home Page ------------------
def run():
    st.set_page_config(
        page_title="Legal Literacy Portal - Home",
        page_icon="⚖️",
        layout="wide"
    )

    apply_legal_home_styling()

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">⚖️ Legal Literacy Portal</div>
        <div class="hero-subtitle">
            Empowering vulnerable South Africans with knowledge, protection, and access to justice.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Welcome Audio
    play_audio("Welcome to the Legal Literacy Portal! Here you can summarize legal documents, check for fraud, generate a will, and connect with lawyers for safe property transactions.")

    # Quick Stats
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">70%</span>
            <span class="stat-label">South Africans die without having made a will</span>
        </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">40K+</span>
            <span class="stat-label">Documents simplified</span>
        </div>
        """, unsafe_allow_html=True)
    with col_stat3:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">100%</span>
            <span class="stat-label">Free & Accessible</span>
        </div>
        """, unsafe_allow_html=True)

    # Services
    st.markdown("### 🌟 Available Services")
    col1, col2, col3 = st.columns(3)
    with col1:
        create_service_card("📄", "Summarize Legal Documents", "Upload contracts or agreements and get an easy-to-read summary in plain language.", "📥 Summarize Now", "SummarizeDocs", "Opening document summarizer.")
    with col2:
        create_service_card("🔍", "Fraud Detection", "Detect suspicious or predatory clauses in documents using AI and legal rules.", "⚠️ Check Document", "FraudCheck", "Opening fraud detection tool.")
    with col3:
        create_service_card("📝", "Generate a Will", "Enter your family details and assets, and generate a draft will for legal review.", "✍️ Create Will", "WillGen", "Starting will generator.")

    col4, col5 = st.columns(2)
    with col4:
        create_service_card("🏠", "Property & Lawyer Assistance", "Safely sell property or connect with trusted lawyers for advice.", "🏡 Get Assistance", "LawyerAssist", "Opening property and lawyer assistance page.")
    with col5:
        create_service_card("📚", "Know Your Rights", "Interactive guides and lessons on housing, contracts, and legal protection.", "📖 Learn Now", "RightsEdu", "Opening rights education section.")

    # Emergency Contact
    st.markdown("""
    <div class="stats-section">
        <h4 style="color: #FFD700; text-align: center; margin-bottom: 1rem;">
            🆘 Need Urgent Legal Help?
        </h4>
        <div style="text-align: center; color: #FFFFFF;">
            <p><strong>Legal Aid SA Helpline:</strong> 0800 110 110 (Toll Free)</p>
            <p><strong>WhatsApp Help:</strong> 079 835 7179</p>
            <p><strong>Operating Hours:</strong> Monday - Friday, 08:00 - 16:00</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
