import streamlit as st
from gtts import gTTS
import tempfile

def apply_legal_home_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Main app background - Background image with lighter overlay */
    .stApp {
        background: 
            linear-gradient(135deg, rgba(30, 41, 59, 0.65) 0%, rgba(51, 65, 85, 0.55) 50%, rgba(71, 85, 105, 0.50) 100%),
            url('https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
        font-family: 'Inter', sans-serif !important;
        min-height: 100vh !important;
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem !important;
        max-width: 1200px !important;
        background: transparent !important;
    }
    
    /* Force all text to be white and visible */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: white !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
    }
    
    /* Service cards - Brighter background */
    .service-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.20), rgba(255,255,255,0.15)) !important;
        padding: 2.5rem !important;
        border-radius: 20px !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        margin: 1rem 0 !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12) !important;
        backdrop-filter: blur(6px) !important;
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
    }
    
    .service-card:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2) !important;
        border-color: rgba(59, 130, 246, 0.6) !important;
        background: linear-gradient(145deg, rgba(255,255,255,0.25), rgba(255,255,255,0.2)) !important;
    }
    
    .card-icon {
        font-size: 2.5rem !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        display: block !important;
        color: #60A5FA !important;
        font-weight: 600 !important;
    }
    
    .card-title {
        color: white !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 1.2rem !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }
    
    .card-description {
        color: #E2E8F0 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        line-height: 1.7 !important;
        font-size: 1rem !important;
        flex-grow: 1 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6, #1D4ED8) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 2.5rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.35) !important;
        font-size: 1.1rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.45) !important;
    }
    
    /* Stats section - Brighter background */
    .stats-container {
        background: linear-gradient(145deg, rgba(255,255,255,0.20), rgba(255,255,255,0.15)) !important;
        padding: 3rem !important;
        border-radius: 24px !important;
        margin: 4rem 0 !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(6px) !important;
    }
    
    .stat-number {
        color: #60A5FA !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        display: block !important;
        text-shadow: 0 2px 10px rgba(96, 165, 250, 0.3) !important;
    }
    
    .stat-label {
        color: #E2E8F0 !important;
        font-size: 1rem !important;
        margin-top: 0.75rem !important;
        font-weight: 500 !important;
    }
    
    /* Section titles - Background image visible through text */
    .section-title {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin: 4rem 0 3rem !important;
        letter-spacing: -0.01em !important;
        position: relative !important;
        /* Background image visible through text */
        background: url('https://images.unsplash.com/photo-1589829545856-d10d557cf95f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        /* Add text stroke for definition */
        -webkit-text-stroke: 1.5px rgba(255, 255, 255, 0.7) !important;
        text-stroke: 1.5px rgba(255, 255, 255, 0.7) !important;
        /* Enhanced shadow */
        filter: drop-shadow(0 3px 6px rgba(0,0,0,0.4)) drop-shadow(0 6px 12px rgba(0,0,0,0.2)) !important;
    }
    
    .section-title::after {
        content: '' !important;
        position: absolute !important;
        bottom: -10px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100px !important;
        height: 4px !important;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        border-radius: 2px !important;
    }
    
    /* Fallback for section titles */
    @supports not (-webkit-background-clip: text) {
        .section-title {
            color: white !important;
            background: linear-gradient(135deg, #FFFFFF, #CBD5E1) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            -webkit-text-stroke: none !important;
            text-stroke: none !important;
            text-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        }
    }
    
    /* Emergency section - Simplified */
    .emergency-section {
        background: rgba(59, 130, 246, 0.15) !important;
        padding: 2rem !important;
        border-radius: 12px !important;
        margin: 3rem 0 !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        text-align: center !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .emergency-title {
        color: #93C5FD !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-bottom: 1.5rem !important;
    }
    
    .emergency-content p {
        color: white !important;
        margin: 0.5rem 0 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    }
    
    .emergency-content strong {
        color: #93C5FD !important;
        font-weight: 700 !important;
    }

    /* Updated phone number and important text colors in emergency section */
    .emergency-phone {
        font-size: 1.1rem !important; 
        color: #60A5FA !important;
        font-weight: 600 !important;
    }
    
    .emergency-hours {
        font-size: 1rem !important; 
        color: #93C5FD !important;
        font-weight: 500 !important;
    }
    
    /* Info boxes - Lighter */
    [data-testid="stAlert"] {
        background-color: rgba(59, 130, 246, 0.25) !important;
        border: 2px solid rgba(59, 130, 246, 0.5) !important;
        color: white !important;
        backdrop-filter: blur(5px) !important;
    }
    
    [data-testid="stAlert"] p {
        color: white !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    }
    
    /* Footer - Lighter */
    .footer-section {
        text-align: center !important;
        padding: 3rem !important;
        color: #E2E8F0 !important;
        border-top: 2px solid rgba(255,255,255,0.25) !important;
        margin-top: 4rem !important;
        background: rgba(255,255,255,0.05) !important;
        border-radius: 20px 20px 0 0 !important;
    }
    
    .footer-section p {
        color: #E2E8F0 !important;
        margin: 0.75rem 0 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    }
    
    /* Responsive - Adjusted for bigger headings */
    @media (max-width: 768px) {
        .section-title {
            font-size: 2.5rem !important;
        }
        
        .emergency-title {
            font-size: 1.8rem !important;
        }
        
        .main .block-container {
            padding: 1rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .section-title {
            font-size: 2rem !important;
        }
        
        .stat-number {
            font-size: 2.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

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
        st.info("Audio not available")

def run():
    st.set_page_config(
        page_title="Legal Literacy Portal - Empowering South Africans",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    apply_legal_home_styling()

    # Welcome audio section
    st.info("Audio guidance available for enhanced accessibility")
    
    col_audio1, col_audio2, col_audio3 = st.columns([1,2,1])
    with col_audio2:
        if st.button("Play Welcome Message", key="welcome_audio"):
            play_audio("Welcome to the Legal Literacy Portal! This platform helps South Africans understand legal documents, detect fraud, create wills, and connect with trusted lawyers.", auto_play=True)

    # Statistics
    st.markdown("""
    <div class="stats-container">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; text-align: center;">
            <div>
                <span class="stat-number">70%</span>
                <div class="stat-label">South Africans die without a will</div>
            </div>
            <div>
                <span class="stat-number">50K+</span>
                <div class="stat-label">Documents analyzed</div>
            </div>
            <div>
                <span class="stat-number">1000+</span>
                <div class="stat-label">Fraud attempts detected</div>
            </div>
            <div>
                <span class="stat-number">100%</span>
                <div class="stat-label">Free & accessible</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Services Section
    st.markdown('<h2 class="section-title">Legal Protection Services</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="service-card">
            <div class="card-icon"><i class="fas fa-file-contract"></i></div>
            <div class="card-title">Document Summarizer</div>
            <div class="card-description">Transform complex legal documents into clear, understandable summaries in plain English with key highlights.</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Summarize Document", key="summarize"):
            st.session_state['page'] = 'SummarizeDocs'
            play_audio("Opening document summarizer")
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="service-card">
            <div class="card-icon"><i class="fas fa-shield-alt"></i></div>
            <div class="card-title">Fraud Detection</div>
            <div class="card-description">AI-powered analysis to identify suspicious clauses, predatory terms, and potential scams in legal documents.</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Check for Fraud", key="fraud"):
            st.session_state['page'] = 'FraudCheck'
            play_audio("Starting fraud detection")
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="service-card">
            <div class="card-icon"><i class="fas fa-scroll"></i></div>
            <div class="card-title">Will Generator</div>
            <div class="card-description">Create a legally compliant will draft based on South African law, ready for professional review.</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Create Will", key="will"):
            st.session_state['page'] = 'WillGen'
            play_audio("Opening will generator")
            st.rerun()

    # Secondary Services
    st.markdown('<h2 class="section-title">Professional Support</h2>', unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("""
        <div class="service-card">
            <div class="card-icon"><i class="fas fa-gavel"></i></div>
            <div class="card-title">Property & Legal Assistance</div>
            <div class="card-description">Connect with verified lawyers and get guidance for safe property transactions, avoiding common pitfalls.</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Get Professional Help", key="lawyer"):
            st.session_state['page'] = 'LawyerAssist'
            play_audio("Connecting with legal professionals")
            st.rerun()
    
    with col5:
        st.markdown("""
        <div class="service-card">
            <div class="card-icon"><i class="fas fa-balance-scale"></i></div>
            <div class="card-title">Know Your Rights</div>
            <div class="card-description">Interactive legal education covering housing rights, contract law, consumer protection, and essential knowledge.</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Learn Your Rights", key="rights"):
            st.session_state['page'] = 'RightsEdu'
            play_audio("Opening rights education")
            st.rerun()

    # Emergency Section
    st.markdown("""
    <div class="emergency-section">
        <h3 class="emergency-title"><i class="fas fa-exclamation-circle"></i> Need Immediate Legal Help?</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                <div class="emergency-content">
                    <p><strong><i class="fas fa-phone-alt"></i> Legal Aid SA Helpline</strong></p>
                    <p class="emergency-phone">0800 110 110</p>
                    <p>(Toll-Free)</p>
                </div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                <div class="emergency-content">
                    <p><strong><i class="fab fa-whatsapp"></i> WhatsApp Support</strong></p>
                    <p class="emergency-phone">079 835 7179</p>
                    <p>Available 24/7</p>
                </div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                <div class="emergency-content">
                    <p><strong><i class="far fa-clock"></i> Operating Hours</strong></p>
                    <p class="emergency-hours">Mon - Fri</p>
                    <p>08:00 - 16:00</p>
                </div>
            </div>
        </div>
        <p style="margin-top: 1.5rem; font-style: italic; color: #CBD5E1; font-size: 0.9rem;">
            Free legal advice available for qualifying South Africans
        </p>
    </div>
    """, unsafe_allow_html=True)

    
if __name__ == "__main__":
    run()