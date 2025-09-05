# app.py - Enhanced Legal Portal with Font Awesome Icons
import streamlit as st

# Import your page modules
from modules import summarizer, fraud_checker, property_assistance, educational, will_generator, sassa_loan, home

def apply_beautiful_styling():
    """Apply beautiful styling with transparent header design and enhanced navigation"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;500;600;700;800;900&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Beautiful lighter background */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 25%, #E2E8F0 75%, #CBD5E1 100%);
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    
    /* Enhanced animated background overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.12) 0%, transparent 60%),
            radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.12) 0%, transparent 60%),
            radial-gradient(circle at 40% 40%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 60% 70%, rgba(236, 72, 153, 0.06) 0%, transparent 40%);
        pointer-events: none;
        z-index: -1;
        animation: backgroundFloat 20s ease-in-out infinite;
    }
    
    @keyframes backgroundFloat {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; }
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem;
        max-width: 1200px;
    }
    
    /* Transparent Hero Header - No background container */
    .hero-header {
        text-align: center;
        padding: 4rem 2rem 3rem 2rem;
        margin: -2rem -2rem 3rem -2rem;
        position: relative;
        overflow: visible;
    }
    
    /* Keep floating particles effect but make it more subtle */
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(59, 130, 246, 0.15) 2px, transparent 2px),
            radial-gradient(circle at 75% 75%, rgba(139, 92, 246, 0.15) 2px, transparent 2px),
            radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.1) 1px, transparent 1px);
        background-size: 50px 50px, 80px 80px, 30px 30px;
        animation: floatingParticles 30s linear infinite;
        opacity: 0.3;
        pointer-events: none;
    }
    
    @keyframes floatingParticles {
        0% { transform: translateY(0px) translateX(0px); }
        25% { transform: translateY(-20px) translateX(10px); }
        50% { transform: translateY(0px) translateX(-10px); }
        75% { transform: translateY(-10px) translateX(5px); }
        100% { transform: translateY(0px) translateX(0px); }
    }
    
    /* Main title styling - Enhanced for visibility without container */
    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        margin: 0 0 1rem 0 !important;
        background: linear-gradient(135deg, 
            #1E40AF 0%, 
            #3B82F6 25%, 
            #8B5CF6 50%, 
            #EC4899 75%, 
            #10B981 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: titleGlow 3s ease-in-out infinite alternate !important;
        filter: drop-shadow(0 4px 20px rgba(59, 130, 246, 0.4)) drop-shadow(0 2px 8px rgba(255, 255, 255, 0.8)) !important;
        letter-spacing: -0.02em !important;
        line-height: 1.1 !important;
        position: relative;
        z-index: 2;
    }
    
    @keyframes titleGlow {
        0% { 
            filter: drop-shadow(0 4px 20px rgba(59, 130, 246, 0.4)) drop-shadow(0 2px 8px rgba(255, 255, 255, 0.8));
            transform: scale(1);
        }
        100% { 
            filter: drop-shadow(0 6px 30px rgba(139, 92, 246, 0.5)) drop-shadow(0 3px 12px rgba(255, 255, 255, 1));
            transform: scale(1.02);
        }
    }
    
    /* Subtitle styling - Enhanced for visibility */
    .hero-subtitle {
        font-size: 1.4rem !important;
        color: #334155 !important;
        font-weight: 600 !important;
        margin: 0 0 2rem 0 !important;
        letter-spacing: 0.02em !important;
        position: relative;
        z-index: 2;
        animation: subtitleFade 2s ease-out !important;
        text-shadow: 0 2px 4px rgba(255, 255, 255, 0.8), 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    @keyframes subtitleFade {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Feature badges - Enhanced for visibility */
    .feature-badges {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1.5rem;
        position: relative;
        z-index: 2;
    }
    
    .feature-badge {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #1E293B;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15), 0 2px 8px rgba(59, 130, 246, 0.2) !important;
        border: 1px solid rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        animation: badgeFloat 4s ease-in-out infinite;
        backdrop-filter: blur(10px);
    }
    
    .feature-badge:nth-child(1) { animation-delay: 0s; }
    .feature-badge:nth-child(2) { animation-delay: 0.5s; }
    .feature-badge:nth-child(3) { animation-delay: 1s; }
    .feature-badge:nth-child(4) { animation-delay: 1.5s; }
    
    @keyframes badgeFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .feature-badge:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3), 0 4px 12px rgba(0, 0, 0, 0.1);
        background: rgba(59, 130, 246, 0.1);
    }
    
    /* Beautiful page titles */
    .main h1:not(.hero-title) {
        color: #1E293B !important;
        text-align: center !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem !important;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Section headers */
    .main h2 {
        color: #1E40AF !important;
        font-weight: 600 !important;
        border-left: 4px solid #3B82F6 !important;
        padding-left: 1rem !important;
        margin: 2rem 0 1rem 0 !important;
        background: rgba(59, 130, 246, 0.05) !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }
    
    .main h3 {
        color: #7C3AED !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 1rem 0 !important;
    }
    
    /* Beautiful buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6, #1D4ED8) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Form elements */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: rgba(255, 255, 255, 0.8) !important;
        color: #1E293B !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Alert messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 8px !important;
        color: #065F46 !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        color: #1E40AF !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 8px !important;
        color: #92400E !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 8px !important;
        color: #991B1B !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.6) !important;
        border: 2px dashed rgba(59, 130, 246, 0.4) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Cards/containers */
    .stContainer {
        background: rgba(255, 255, 255, 0.7) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* ENHANCED SIDEBAR STYLING - COMPLETE GRADIENT COVERAGE */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #3B82F6 0%, #8B5CF6 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Remove all white/grey backgrounds from sidebar */
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        background: transparent !important;
        padding: 1rem 0.75rem !important;
    }
    
    /* Fix selectbox (fallback navigation) background */
    section[data-testid="stSidebar"] .stSelectbox {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox select {
        background: transparent !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox select:focus {
        background: rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Fix any remaining white containers in sidebar */
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="element-container"] {
        background: transparent !important;
    }
    
    /* Force all sidebar elements to transparent background */
    section[data-testid="stSidebar"] * {
        background-color: transparent !important;
    }
    
    /* Exception for specific interactive elements that need subtle backgrounds */
    section[data-testid="stSidebar"] .nav-link,
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] select {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    section[data-testid="stSidebar"] .nav-link:hover,
    section[data-testid="stSidebar"] button:hover,
    section[data-testid="stSidebar"] select:hover {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] .nav-link-selected,
    section[data-testid="stSidebar"] button:focus,
    section[data-testid="stSidebar"] select:focus {
        background: rgba(255, 255, 255, 0.25) !important;
    }
    
    /* Option menu styling - Enhanced */
    .nav-link {
        color: white !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        margin: 0.25rem 0 !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        border-left: 3px solid transparent !important;
    }
    
    .nav-link:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        border-left: 3px solid white !important;
        transform: translateX(5px);
    }
    
    .nav-link-selected {
        background: rgba(255, 255, 255, 0.25) !important;
        border-left: 3px solid white !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Text colors */
    .main p, .main span, .main div {
        color: #475569 !important;
    }
    
    .main strong {
        color: #1E293B !important;
    }
    
    /* Sidebar text colors - Force white text everywhere */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Specifically target common text elements */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] option {
        color: white !important;
        background: transparent !important;
    }
    
    /* Links */
    .main a {
        color: #3B82F6 !important;
        text-decoration: none !important;
    }
    
    .main a:hover {
        color: #60A5FA !important;
        text-decoration: underline !important;
    }
    
    /* Footer styling */
    .footer-section {
        text-align: center !important;
        padding: 3rem !important;
        color: #475569 !important;
        border-top: 2px solid rgba(59, 130, 246, 0.25) !important;
        margin-top: 4rem !important;
        background: rgba(255, 255, 255, 0.6) !important;
        border-radius: 20px 20px 0 0 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .footer-section p {
        color: #475569 !important;
        margin: 0.75rem 0 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
        
        .hero-title {
            font-size: 3rem !important;
        }
        
        .hero-subtitle {
            font-size: 1.1rem !important;
        }
        
        .hero-header {
            padding: 2rem 1rem !important;
            margin: -1rem -1rem 2rem -1rem !important;
        }
        
        .feature-badges {
            gap: 0.5rem;
        }
        
        .feature-badge {
            font-size: 0.8rem;
            padding: 0.4rem 0.8rem;
        }
        
        .footer-section {
            padding: 2rem 1rem !important;
            margin-top: 2rem !important;
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding: 1rem 0.5rem !important;
        }
    }
    
    /* Tablet responsive */
    @media (max-width: 1024px) and (min-width: 769px) {
        .hero-title {
            font-size: 3.5rem !important;
        }
        
        .hero-subtitle {
            font-size: 1.2rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def show_hero_header():
    """Display the hero header - call this only on the home page"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title"><i class="fas fa-balance-scale"></i> Legal Literacy Portal</h1>
        <p class="hero-subtitle">Empowering South Africans with Professional Legal Knowledge & Services</p>
        <div class="feature-badges">
            <span class="feature-badge"><i class="fas fa-shield-alt"></i> Fraud Protection</span>
            <span class="feature-badge"><i class="fas fa-file-contract"></i> Document Analysis</span>
            <span class="feature-badge"><i class="fas fa-hand-holding-usd"></i> SASSA Support</span>
            <span class="feature-badge"><i class="fas fa-home"></i> Property Law</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Configure the app
st.set_page_config(
    page_title="Legal Literacy Portal - Professional Legal Services",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply styling
apply_beautiful_styling()

# ------------------- Navigation -------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <h2 style="color: white !important; margin: 0; font-size: 1.5rem; font-weight: 700;">
            <i class="fas fa-balance-scale"></i> Legal Tools
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    selected = st.selectbox(
        "Choose a tool:",
        options=[
            "Home", 
            "Document Summarizer", 
            "Fraud Detection", 
            "Will Generator", 
            "Property & Legal Help", 
            "Know Your Rights", 
            "SASSA Loan Assistant"
        ],
        label_visibility="collapsed"
    )

# ------------------- Page Routing -------------------
if selected == "Home":
    show_hero_header()
    home.run()
elif selected == "Document Summarizer":
    st.title("Document Summarizer")
    summarizer.run()
elif selected == "Fraud Detection":
    st.title("Fraud Detection")
    fraud_checker.run()
elif selected == "Will Generator":
    st.title("Will Generator")
    will_generator.run()
elif selected == "Property & Legal Help":
    st.title("Property & Legal Help")
    property_assistance.run()
elif selected == "Know Your Rights":
    st.title("Know Your Rights")
    educational.run()
elif selected == "SASSA Loan Assistant":
    st.title("SASSA Loan Assistant")
    sassa_loan.run()

# Enhanced Transparent Footer
st.markdown("""
    <div class="footer-section">
        <p><i class="fas fa-balance-scale"></i> Legal Literacy Portal</p>
        <p>Empowering South Africans through legal knowledge</p>
        <p>© 2025 Legal Literacy Portal. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
