# app.py - Fixed Legal Portal with Visible Navigation
import streamlit as st

# Import your page modules
from pages import summarizer, fraud_checker, property_assistance, educational, will_generator, sassa_loan, login

def apply_beautiful_styling():
    """Apply beautiful styling without breaking navigation"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Beautiful lighter background */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 25%, #E2E8F0 75%, #CBD5E1 100%);
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    
    /* Animated background overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem;
        max-width: 1200px;
    }
    
    /* Beautiful page titles */
    .main h1 {
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
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
        
        .main h1 {
            font-size: 2rem !important;
        }
    }
    </style>
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

# Add a simple header in the main content area
st.markdown("""
<div style="text-align: center; padding: 2rem 0; border-bottom: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #3B82F6, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        ⚖️ Legal Literacy Portal
    </h1>
    <p style="color: #64748B; font-size: 1.1rem; margin: 0.5rem 0 0 0;">
        Empowering South Africans with Legal Knowledge
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------- Pages with Icons ------------------- 
pages = {
    "Home": [st.Page("pages/home.py", title="🏠 Home")],
    "Legal Tools": [
        st.Page("pages/summarizer.py", title="📄 Document Summarizer"),
        st.Page("pages/sassa_loan.py", title="💰 SASSA Loan Assistant"),
        st.Page("pages/fraud_checker.py", title="🛡️ Fraud Detection"),
        st.Page("pages/will_generator.py", title="📜 Will Generator"),
        st.Page("pages/property_assistance.py", title="🏡 Property & Legal Help"),
        st.Page("pages/educational.py", title="📚 Know Your Rights"),
    ]
}

# Create navigation - this should show in the sidebar
selected_page = st.navigation(pages)

# Show current page info


# ------------------- Routing ------------------- 
if selected_page.title == "🏠 Home":
    import pages.home as home
    home.run()
elif selected_page.title == "📄 Document Summarizer":
    summarizer.run()
elif selected_page.title == "🛡️ Fraud Detection":
    fraud_checker.run()
elif selected_page.title == "📜 Will Generator":
    will_generator.run()
elif selected_page.title == "🏡 Property & Legal Help":
    st.info("🚧 Property & Legal Help coming soon! This feature is being developed to connect you with verified legal professionals.")
elif selected_page.title == "📚 Know Your Rights":
    educational.run()
elif selected_page.title == "💰 SASSA Loan Assistant":
    sassa_loan.run()

# Footer
st.markdown("""
---
<div style="text-align: center; color: #64748B; padding: 2rem 0;">
    <p>🇿🇦 Proudly serving South African communities</p>
    <p style="font-size: 0.9rem;">This platform provides educational information and should not replace professional legal advice</p>
</div>
""", unsafe_allow_html=True)