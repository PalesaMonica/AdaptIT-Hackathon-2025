import streamlit as st
from gtts import gTTS
import tempfile

# ---------------- SASSA Styling ----------------
def apply_sassa_home_styling():
    st.markdown("""
    <style>
    /* Main background with SASSA colors */
    .main .block-container {
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #2E8B57 0%, #1F5F3F 50%, #228B22 100%);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Hero section styling */
    .hero-section {
        background: linear-gradient(45deg, rgba(255,215,0,0.15), rgba(255,255,255,0.1));
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
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        color: #FFFFFF;
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* Service cards styling */
    .service-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid rgba(255,215,0,0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
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
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    .card-description {
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Button styling */
    .service-button {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #1F5F3F;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3);
    }
    
    .service-button:hover {
        background: linear-gradient(45deg, #FFA500, #FFD700);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,215,0,0.5);
    }
    
    /* Override default Streamlit button styling */
    .stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        color: #1F5F3F !important;
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
    
    /* Audio player styling */
    .stAudio {
        margin: 1rem 0;
    }
    
    /* Quick stats section */
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
    
    /* Features section */
    .features-section {
        background: rgba(46,139,87,0.2);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid rgba(255,215,0,0.2);
    }
    
    .feature-item {
        color: #FFFFFF;
        margin: 1rem 0;
        padding: 0.8rem;
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        border-left: 4px solid #FFD700;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
        }
        .service-card {
            padding: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Audio Guidance ----------------
def play_audio(text="Welcome to the SASSA Portal!"):
    try:
        tts = gTTS(text=text, lang="en")
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        st.audio(tmp_file.name, format="audio/mp3")
    except:
        st.warning("🔇 Audio guidance unavailable")

# ---------------- Service Cards Component ----------------
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
        # Play audio feedback
        try:
            tts = gTTS(text=audio_text, lang="en")
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp_file.name)
            st.audio(tmp_file.name, format="audio/mp3")
        except:
            pass

# ------------------Home Page ------------------
def run():
    st.set_page_config(
        page_title="SASSA Portal - Home",
        page_icon="🇿🇦",
        layout="wide"
    )
    
    apply_sassa_home_styling()
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🇿🇦 SASSA Digital Portal</div>
        <div class="hero-subtitle">
            Access South African Social Security Agency - Anytime, Anywhere
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome audio
    st.markdown("### 🔊 Welcome Message")
    play_audio("Welcome to the SASSA Digital Portal! Your one-stop solution for South African social security services. Navigate through the options below to apply for grants, track applications, or book appointments.")
    
    # Quick Stats
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">17.4M</span>
            <span class="stat-label">Applications Processed</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">80K</span>
            <span class="stat-label">Monthly New Applications</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">24/7</span>
            <span class="stat-label">Service Availability</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat4:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">100%</span>
            <span class="stat-label">Digital Access</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Service Cards Section
    st.markdown("### 🌟 Available Services")
    
    # Row 1: Main Services
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_service_card(
            "📝", 
            "Apply for Grants",
            "AI-powered application assistance with OCR technology for easy form filling. Upload documents and get instant help.",
            "🚀 Start Application",
            "AI Assistance",
            "Starting grant application process with AI assistance."
        )
    
    with col2:
        create_service_card(
            "📍", 
            "Track Application",
            "Real-time status updates on your grant applications. Check progress and receive important notifications.",
            "🔍 Track Status",
            "Track Application", 
            "Opening application tracking service."
        )
    
    with col3:
        create_service_card(
            "📅", 
            "Book Appointments",
            "Schedule appointments for identity verification, biometric capture, or document collection at your nearest SASSA office.",
            "📋 Book Appointment",
            "Booking",
            "Opening appointment booking system."
        )
    
    # Row 2: Additional Services
    col4, col5 = st.columns(2)
    
    with col4:
        create_service_card(
            "📱", 
            "USSD Services", 
            "Access SASSA services using any mobile phone. No smartphone or internet connection required - just dial our USSD code.",
            "📞 Try USSD Demo",
            "USSD Demo",
            "Opening USSD service demonstration."
        )
    
    with col5:
        create_service_card(
            "📄", 
            "Download Documents",
            "Access and download official SASSA forms, application documents, and important notices in multiple languages.",
            "⬇️ Download Forms",
            "Download Document",
            "Opening document download section."
        )
    
    # Features Section
    st.markdown("""
    <div class="features-section">
        <h3 style="color: #FFD700; text-align: center; margin-bottom: 1.5rem;">
            ✨ Why Choose SASSA Digital Portal?
        </h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
            <div class="feature-item">
                <strong>🌐 Universal Access:</strong> Works on smartphones, basic phones, and computers
            </div>
            <div class="feature-item">
                <strong>🤖 AI-Powered:</strong> Smart assistance for form filling and document processing
            </div>
            <div class="feature-item">
                <strong>🔒 Secure & Private:</strong> Bank-level security for your personal information
            </div>
            <div class="feature-item">
                <strong>🌍 Multi-Language:</strong> Available in all official South African languages
            </div>
            <div class="feature-item">
                <strong>♿ Accessible Design:</strong> Built for users with disabilities and low literacy
            </div>
            <div class="feature-item">
                <strong>⚡ Real-Time Updates:</strong> Instant notifications and status updates
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Emergency Contact
    st.markdown("""
    <div class="stats-section">
        <h4 style="color: #FFD700; text-align: center; margin-bottom: 1rem;">
            🆘 Need Immediate Help?
        </h4>
        <div style="text-align: center; color: #FFFFFF;">
            <p><strong>SASSA Helpline:</strong> 0800 60 10 11 (Toll Free)</p>
            <p><strong>Emergency USSD:</strong> *120*32390# (From any phone)</p>
            <p><strong>Operating Hours:</strong> Monday - Friday, 08:00 - 17:00</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

