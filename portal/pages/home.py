import streamlit as st
from gtts import gTTS
import tempfile

# ---------------- Professional Legal Styling ----------------
def apply_legal_home_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main container with professional gradient */
    .main .block-container {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
        min-height: 100vh;
    }
    
    /* Hero section - clean and professional */
    .hero-section {
        background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.2);
    }
    
    .hero-title {
        color: #051cf0;
        font-size: 3.5rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        color: #515263;
        font-size: 1.25rem;
        font-weight: 400;
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto 2rem;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #3B82F6, #1D4ED8);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    /* Service cards - professional card design */
    .service-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(20px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .service-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6, #EF4444);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .service-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .service-card:hover::before {
        opacity: 1;
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        display: block;
        text-align: center;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .card-title {
        color: #F8FAFC;
        font-size: 1.375rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1rem;
        line-height: 1.3;
    }
    
    .card-description {
        color: #94A3B8;
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* Professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 2rem !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        letter-spacing: 0.025em !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Stats section - modern card design */
    .stats-container {
        background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
        padding: 2rem;
        border-radius: 20px;
        margin: 3rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
        border-radius: 12px;
        background: rgba(255,255,255,0.05);
        margin: 0.5rem;
        transition: transform 0.3s ease;
    }
    
    .stat-item:hover {
        transform: scale(1.05);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: block;
        line-height: 1.1;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #94A3B8;
        font-weight: 400;
        margin-top: 0.5rem;
        line-height: 1.4;
    }
    
    /* Section headers */
    .section-title {
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        margin: 3rem 0 2rem;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -0.5rem;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6);
        border-radius: 2px;
    }
    
    /* Emergency contact - professional alert */
    .emergency-section {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.05));
        padding: 2rem;
        border-radius: 16px;
        margin: 3rem 0;
        border: 1px solid rgba(239, 68, 68, 0.2);
        backdrop-filter: blur(20px);
    }
    
    .emergency-title {
        color: #FCA5A5;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .emergency-content {
        text-align: center;
        color: #F8FAFC;
    }
    
    .emergency-content p {
        margin: 0.75rem 0;
        font-weight: 400;
    }
    
    .emergency-content strong {
        color: #FCA5A5;
        font-weight: 500;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.125rem;
        }
        
        .service-card {
            padding: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Enhanced Audio Guidance ----------------
def play_audio(text="Welcome to the Legal Literacy Portal!", auto_play=False):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        
        if auto_play:
            st.audio(tmp_file.name, format="audio/mp3", autoplay=True)
        else:
            st.audio(tmp_file.name, format="audio/mp3")
    except Exception as e:
        st.info("Click the audio controls above to hear guidance")

# ---------------- Enhanced Service Cards ----------------
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
        # Audio feedback for navigation
        play_audio(audio_text)
        st.rerun()

# ------------------ Enhanced Home Page ------------------
def run():
    st.set_page_config(
        page_title="Legal Literacy Portal - Empowering South Africans",
        page_icon="⚖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    apply_legal_home_styling()

    # Hero Section with enhanced content
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">Trusted by South Africans</div>
        <div class="hero-title">Legal Literacy Portal</div>
        <div class="hero-subtitle">
            Empowering vulnerable South Africans with accessible legal knowledge, 
            document protection, and connections to trusted legal professionals.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Welcome audio with better UX
    st.info("Enable audio for guided navigation and accessibility features")
    if st.button("Play Welcome Message", key="welcome_audio"):
        play_audio("Welcome to the Legal Literacy Portal! This platform helps South Africans understand legal documents, detect fraud, create wills, and connect with trusted lawyers. Use the services below to get started.", auto_play=True)

    # Enhanced statistics
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">70%</span>
            <span class="stat-label">South Africans die without a will</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">50K+</span>
            <span class="stat-label">Documents analyzed</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">1000+</span>
            <span class="stat-label">Fraud attempts detected</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat4:
        st.markdown("""
        <div class="stat-item">
            <span class="stat-number">100%</span>
            <span class="stat-label">Free & accessible</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Services section with better organization
    st.markdown('<h2 class="section-title">Legal Protection Services</h2>', unsafe_allow_html=True)
    
    # Primary services
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_service_card(
            "", 
            "Document Summarizer", 
            "Transform complex legal documents into clear, understandable summaries in plain English with key highlights.",
            "Summarize Document", 
            "SummarizeDocs", 
            "Opening the document summarizer to help you understand legal documents clearly."
        )
    
    with col2:
        create_service_card(
            "", 
            "Fraud Detection", 
            "AI-powered analysis to identify suspicious clauses, predatory terms, and potential scams in legal documents.",
            "Check for Fraud", 
            "FraudCheck", 
            "Starting fraud detection to protect you from suspicious legal documents."
        )
    
    with col3:
        create_service_card(
            "", 
            "Will Generator", 
            "Create a legally compliant will draft based on South African law, ready for professional review and notarization.",
            "Create Will", 
            "WillGen", 
            "Opening the will generator to help you create your legal will."
        )

    # Secondary services
    st.markdown('<h2 class="section-title">Professional Support</h2>', unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    
    with col4:
        create_service_card(
            "", 
            "Property & Legal Assistance", 
            "Connect with verified lawyers and get guidance for safe property transactions, avoiding common pitfalls and scams.",
            "Get Professional Help", 
            "LawyerAssist", 
            "Connecting you with professional legal assistance for property matters."
        )
    
    with col5:
        create_service_card(
            "", 
            "Know Your Rights", 
            "Interactive legal education covering housing rights, contract law, consumer protection, and essential legal knowledge.",
            "Learn Your Rights", 
            "RightsEdu", 
            "Opening the rights education section to teach you about your legal protections."
        )

    # Emergency contact section with better design
    st.markdown("""
    <div class="emergency-section">
        <h3 class="emergency-title">
            Need Immediate Legal Help?
        </h3>
        <div class="emergency-content">
            <p><strong>Legal Aid SA Helpline:</strong> 0800 110 110 (Toll-Free)</p>
            <p><strong>WhatsApp Support:</strong> 079 835 7179</p>
            <p><strong>Operating Hours:</strong> Monday - Friday, 08:00 - 16:00</p>
            <p style="margin-top: 1rem; font-style: italic; color: #CBD5E1;">
                Free legal advice available for qualifying South Africans
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer information
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #64748B; border-top: 1px solid rgba(0,0,0,0.1); margin-top: 3rem;">
        <p>Proudly serving South African communities | Built with accessibility and inclusion in mind</p>
        <p style="font-size: 0.875rem; margin-top: 0.5rem;">
            This platform provides educational information and should not replace professional legal advice
        </p>
    </div>
    """, unsafe_allow_html=True)
