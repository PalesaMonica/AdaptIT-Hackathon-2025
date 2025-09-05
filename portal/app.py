# app.py - Enhanced Legal Portal with Conditional Header
import streamlit as st

# Import your page modules
from pages import summarizer, fraud_checker, property_assistance, educational, will_generator, sassa_loan, login

def apply_beautiful_styling():
    """Apply beautiful styling with transparent header design"""
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
        /* Removed background, border-radius, box-shadow, backdrop-filter, and border */
        position: relative;
        overflow: visible; /* Changed from hidden to visible */
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
        opacity: 0.3; /* Reduced opacity */
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
        /* Enhanced text shadow for better visibility */
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
        color: #334155 !important; /* Darker for better contrast */
        font-weight: 600 !important; /* Increased weight */
        margin: 0 0 2rem 0 !important;
        letter-spacing: 0.02em !important;
        position: relative;
        z-index: 2;
        animation: subtitleFade 2s ease-out !important;
        /* Enhanced text shadow for visibility */
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
        background: rgba(255, 255, 255, 0.95) !important; /* Increased opacity */
        color: #1E293B;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15), 0 2px 8px rgba(59, 130, 246, 0.2) !important; /* Enhanced shadow */
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
    
    /* Sidebar styling - Light theme */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border-right: 1px solid rgba(59, 130, 246, 0.2) !important;
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Text colors */
    .main p, .main span, .main div {
        color: #475569 !important;
    }
    
    .main strong {
        color: #1E293B !important;
    }
    
    /* Sidebar text colors */
    section[data-testid="stSidebar"] * {
        color: #1E293B !important;
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
    
    /* Footer styling - Added to match the design */
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
    initial_sidebar_state="expanded"  # This ensures sidebar is visible
)

# Apply styling
apply_beautiful_styling()

# ------------------- Pages with Icons ------------------- 
pages = {
    "Home": [st.Page("pages/home.py", title="Home")],
    "Legal Tools": [
        st.Page("pages/summarizer.py", title="Document Summarizer"),
        st.Page("pages/sassa_loan.py", title="SASSA Loan Assistant"),
        st.Page("pages/fraud_checker.py", title="Fraud Detection"),
        st.Page("pages/will_generator.py", title="Will Generator"),
        st.Page("pages/property_assistance.py", title="Property & Legal Help"),
        st.Page("pages/educational.py", title="Know Your Rights"),
    ]
}

# Create navigation - this should show in the sidebar
selected_page = st.navigation(pages)

# ------------------- Routing ------------------- 
if selected_page.title == "Home":
    # Show hero header only on home page
    show_hero_header()
    import pages.home as home
    home.run()
elif selected_page.title == "Document Summarizer":
    summarizer.run()
elif selected_page.title == "Fraud Detection":
    fraud_checker.run()
elif selected_page.title == "Will Generator":
    will_generator.run()
elif selected_page.title == "Property & Legal Help":
    property_assistance.run()
elif selected_page.title == "Know Your Rights":
    educational.run()
elif selected_page.title == "SASSA Loan Assistant":
    sassa_loan.run()

# Enhanced Transparent Footer
st.markdown("""
    <div class="footer-section">
        <p><i class="fas fa-balance-scale"></i> Legal Literacy Portal</p>
        <p>Empowering South Africans through legal knowledge</p>
        <p>© 2025 Legal Literacy Portal. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
