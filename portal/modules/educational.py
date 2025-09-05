# pages/educational.py - Know Your Rights Module
import streamlit as st

def apply_educational_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 25%, #CBD5E1 50%, #94A3B8 75%, #64748B 100%);
        min-height: 100vh;
        color: #1E293B;
    }
    
    /* Elegant Blue-to-Pink Gradient Heading */
    .stMarkdown h1, .main h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 3.5rem !important;
        text-align: center !important;
        letter-spacing: -0.02em !important;
        margin: 2rem 0 2.5rem 0 !important;
        padding: 1.5rem 0 !important;
        position: relative !important;
        background: linear-gradient(135deg, 
            #1E40AF 0%,
            #3B82F6 15%,
            #6366F1 30%,
            #8B5CF6 45%,
            #A855F7 60%,
            #C026D3 75%,
            #E879F9 90%,
            #F472B6 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-shadow: 
            0 2px 10px rgba(30, 64, 175, 0.4),
            0 4px 20px rgba(244, 114, 182, 0.3) !important;
        filter: drop-shadow(0 0 15px rgba(139, 92, 246, 0.3)) !important;
    }
    
    /* Subtle Blue-Pink Accent Lines */
    .stMarkdown h1::before, .main h1::before {
        content: '' !important;
        position: absolute !important;
        top: -8px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 60% !important;
        height: 3px !important;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #1E40AF 30%, 
            #8B5CF6 50%, 
            #F472B6 70%, 
            transparent 100%) !important;
        border-radius: 2px !important;
        opacity: 0.8 !important;
    }
    
    .stMarkdown h1::after, .main h1::after {
        content: '' !important;
        position: absolute !important;
        bottom: -8px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 40% !important;
        height: 3px !important;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #3B82F6 25%, 
            #A855F7 50%, 
            #F472B6 75%, 
            transparent 100%) !important;
        border-radius: 2px !important;
        opacity: 0.6 !important;
    }
    
    /* Improved Section Headings */
    .main h2, .main h3 {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        border-left: 4px solid #3B82F6 !important;
        padding-left: 1rem !important;
        margin: 2rem 0 1rem 0 !important;
        text-shadow: none !important;
        background: linear-gradient(145deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.05)) !important;
        padding: 0.75rem 1rem !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    /* Enhanced Text Visibility */
    .main p, .main li, .main div {
        color: #1E293B !important;
        line-height: 1.7 !important;
        text-shadow: none !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    /* Stronger text for important content */
    .main strong, .main b {
        color: #0F172A !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }
    
    .rights-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1rem 0 !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08) !important;
        border: 2px solid rgba(59, 130, 246, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .rights-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.15) !important;
        background: linear-gradient(145deg, rgba(59, 130, 246, 0.05), rgba(59, 130, 246, 0.02)) !important;
    }
    
    .rights-card-human {
        border-left: 6px solid #1E40AF !important;
    }
    
    .rights-card-constitutional {
        border-left: 6px solid #8B5CF6 !important;
    }
    
    .rights-card-civil {
        border-left: 6px solid #22C55E !important;
    }
    
    .rights-card-worker {
        border-left: 6px solid #F59E0B !important;
    }
    
    .rights-card-consumer {
        border-left: 6px solid #06B6D4 !important;
    }
    
    .rights-card-family {
        border-left: 6px solid #EC4899 !important;
    }
    
    .rights-card-digital {
        border-left: 6px solid #6366F1 !important;
    }
    
    .rights-card-legal {
        border-left: 6px solid #EF4444 !important;
    }
    
    .emergency-box {
        background: linear-gradient(145deg, rgba(30, 64, 175, 0.95), rgba(30, 58, 138, 0.9)) !important;
        color: white !important;
        border-left: 6px solid #1E3A8A !important;
        padding: 2rem !important;
        margin: 2rem 0 !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(30, 64, 175, 0.2) !important;
        backdrop-filter: blur(8px) !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .emergency-box h3 {
        color: white !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .emergency-box p, .emergency-box strong {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
    }
    
    .detail-box {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        border: 2px solid rgba(59, 130, 246, 0.2) !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05) !important;
    }
    
    .detail-box h3 {
        color: #1E40AF !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        text-shadow: none !important;
        background: none !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .category-title {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        color: #1E293B !important;
        margin-bottom: 0.5rem !important;
        text-shadow: none !important;
    }
    
    .category-desc {
        font-size: 1rem !important;
        color: #475569 !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
        text-shadow: none !important;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #F472B6 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3) !important;
        letter-spacing: 0.025em !important;
        width: 100% !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1E40AF 0%, #7C3AED 50%, #EC4899 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Back Button Styling */
    .back-button {
        background: rgba(255,255,255,0.9) !important;
        color: #1E40AF !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        backdrop-filter: blur(4px) !important;
    }
    
    .back-button:hover {
        background: rgba(59, 130, 246, 0.1) !important;
        border-color: #3B82F6 !important;
        color: #1E40AF !important;
    }
    
    /* Context Cards */
    .context-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        margin: 1.5rem 0 !important;
        border-left: 5px solid #1E40AF !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .context-card h4 {
        color: #1E40AF !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-shadow: none !important;
    }
    
    .context-card ul {
        margin: 1rem 0 0 0 !important;
        padding-left: 1.5rem !important;
    }
    
    .context-card li {
        color: #334155 !important;
        margin: 0.75rem 0 !important;
        line-height: 1.7 !important;
        font-size: 1rem !important;
        text-shadow: none !important;
        font-weight: 500 !important;
    }
    
    .context-card li strong {
        color: #3B82F6 !important;
        font-weight: 700 !important;
    }
    
    /* Enhanced Alert Boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 12px !important;
        font-weight: 600 !important;
        text-shadow: none !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .stSuccess {
        background: rgba(34, 197, 94, 0.1) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        color: #166534 !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #1E40AF !important;
    }
    
    .stWarning {
        background: rgba(244, 114, 182, 0.1) !important;
        border: 1px solid rgba(244, 114, 182, 0.3) !important;
        color: #BE185D !important;
    }
    
    .stError {
        background: rgba(30, 64, 175, 0.1) !important;
        border: 1px solid rgba(30, 64, 175, 0.3) !important;
        color: #1E40AF !important;
    }
    
    /* Resources section */
    .resources-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .resource-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(248,250,252,0.9)) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        border-left: 4px solid #3B82F6 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .resource-card h4 {
        color: #1E40AF !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }
    
    .resource-card ul {
        margin: 0 !important;
        padding-left: 1rem !important;
    }
    
    .resource-card li {
        color: #475569 !important;
        margin: 0.5rem 0 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        text-shadow: none !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stMarkdown h1, .main h1 {
            font-size: 2.5rem !important;
        }
        
        .main .block-container {
            padding: 1rem 1.5rem !important;
        }
        
        .rights-card {
            padding: 1.5rem !important;
        }
        
        .resources-grid {
            grid-template-columns: 1fr !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def run():
    """
    Main function called by app.py when "Know Your Rights" page is selected
    """
    
    # Apply consistent styling
    apply_educational_styling()

    # Initialize session state for this page
    if 'selected_rights_category' not in st.session_state:
        st.session_state.selected_rights_category = None

    # Rights categories data with neutral descriptions
    rights_categories = {
        'Human Rights': {
            'description': 'Universal rights inherent to all human beings',
            'examples': ['Right to life', 'Freedom from torture', 'Right to education', 'Freedom of expression'],
            'css_class': 'rights-card-human'
        },
        'Constitutional Rights': {
            'description': 'Rights protected by your constitution',
            'examples': ['Freedom of speech', 'Right to privacy', 'Due process', 'Equal protection'],
            'css_class': 'rights-card-constitutional'
        },
        'Civil Rights': {
            'description': 'Rights to participate in society without discrimination',
            'examples': ['Anti-discrimination', 'Voting rights', 'Access to public services', 'Fair housing'],
            'css_class': 'rights-card-civil'
        },
        'Worker Rights': {
            'description': 'Rights in the workplace and employment',
            'examples': ['Fair wages', 'Safe working conditions', 'Right to organize', 'Protection from harassment'],
            'css_class': 'rights-card-worker'
        },
        'Consumer Rights': {
            'description': 'Rights when purchasing goods and services',
            'examples': ['Right to refund', 'Product safety', 'Fair pricing', 'Privacy protection'],
            'css_class': 'rights-card-consumer'
        },
        'Family Rights': {
            'description': 'Rights related to family, marriage, and children',
            'examples': ['Parental rights', 'Child protection', 'Marriage equality', 'Custody rights'],
            'css_class': 'rights-card-family'
        },
        'Digital Rights': {
            'description': 'Rights in the digital age and online spaces',
            'examples': ['Data privacy', 'Digital access', 'Online freedom', 'Cybersecurity protection'],
            'css_class': 'rights-card-digital'
        },
        'Legal Proceedings': {
            'description': 'Rights when dealing with courts and law enforcement',
            'examples': ['Right to counsel', 'Right to remain silent', 'Fair trial', 'Presumption of innocence'],
            'css_class': 'rights-card-legal'
        }
    }

    # Page header
    st.markdown("# Know Your Rights")
    st.markdown("### Understanding your rights is the foundation of justice. Explore different categories to learn about your legal protections and freedoms.")
    st.markdown("---")

    # Rights categories grid
    if not st.session_state.selected_rights_category:
        st.markdown("## Rights Categories")
        st.markdown("*Click on any category below to learn more*")
        
        # Create columns for grid layout
        cols = st.columns(2)  # 2 columns for better mobile experience
        
        for i, (category, info) in enumerate(rights_categories.items()):
            with cols[i % 2]:
                # Create custom styled button using markdown and button
                st.markdown(f"""
                <div class="rights-card {info['css_class']}">
                    <div class="category-title">{category}</div>
                    <div class="category-desc">{info['description']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Learn about {category}", key=f"btn_{category}", use_container_width=True):
                    st.session_state.selected_rights_category = category
                    st.rerun()
                
                st.markdown("---")

    # Selected category details
    if st.session_state.selected_rights_category:
        selected = st.session_state.selected_rights_category
        info = rights_categories[selected]
        
        # Back button at top
        col_back, col_title = st.columns([1, 4])
        with col_back:
            if st.button("Back", type="secondary", key="back_btn"):
                st.session_state.selected_rights_category = None
                st.rerun()
        
        with col_title:
            st.markdown(f"## {selected}")
        
        st.markdown(f"**{info['description']}**")
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Key Areas Include:")
            for example in info['examples']:
                st.markdown(f"• {example}")
            
            # Add South African context
            st.markdown("### South African Context:")
            if selected == "Human Rights":
                st.markdown("• Protected by Chapter 2 of the Constitution")
                st.markdown("• Enforced by the Human Rights Commission")
                st.markdown("• Constitutional Court as final arbiter")
            elif selected == "Constitutional Rights":
                st.markdown("• Bill of Rights in the Constitution")
                st.markdown("• 27 fundamental rights guaranteed")
                st.markdown("• Can approach Constitutional Court directly")
            elif selected == "Worker Rights":
                st.markdown("• Labour Relations Act protection")
                st.markdown("• Basic Conditions of Employment Act")
                st.markdown("• CCMA for dispute resolution")
            elif selected == "Consumer Rights":
                st.markdown("• Consumer Protection Act (CPA)")
                st.markdown("• National Consumer Commission")
                st.markdown("• Consumer Tribunal for disputes")
            else:
                st.markdown("• Protected under South African law")
                st.markdown("• Various Acts and regulations apply")
                st.markdown("• Courts provide remedy for violations")
        
        with col2:
            st.markdown('<div class="detail-box">', unsafe_allow_html=True)
            st.markdown("### Quick Actions")
            
            if st.button("Learn the Basics", use_container_width=True):
                st.info("Essential information everyone should know about this area of rights")
            
            if st.button("Common Scenarios", use_container_width=True):
                st.info("Real-world situations and how to handle them effectively")
            
            if st.button("Know When to Get Help", use_container_width=True):
                st.info("When to contact a lawyer, legal aid, or advocacy group")
            
            if st.button("Find Resources", use_container_width=True):
                st.info("Links to relevant government departments and NGOs")
            
            st.markdown('</div>', unsafe_allow_html=True)

    # Emergency Rights Section - Always visible
    st.markdown("---")
    st.markdown('<div class="emergency-box">', unsafe_allow_html=True)
    st.markdown("### Emergency Rights Reminder")
    st.markdown("In any interaction with law enforcement or legal proceedings, remember these fundamental rights:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("• **Right to remain silent** - You don't have to answer questions")
        st.markdown("• **Right to an attorney** - Legal representation is your right")

    with col2:
        st.markdown("• **Refuse searches without warrant** - Unless lawfully required")
        st.markdown("• **Know why you're detained** - Police must inform you")

    st.markdown("**Important Numbers:** Legal Aid SA: 0800 110 110 | Police: 10111 | Emergency: 112")
    st.markdown('</div>', unsafe_allow_html=True)

    # Resources section
    st.markdown("---")
    st.markdown("## Helpful Resources")
    
    st.markdown('<div class="resources-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="resource-card">
            <h4>Government</h4>
            <ul>
                <li>Department of Justice</li>
                <li>Human Rights Commission</li>
                <li>Public Protector</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="resource-card">
            <h4>Legal Aid</h4>
            <ul>
                <li>Legal Aid South Africa</li>
                <li>ProBono.Org</li>
                <li>University Law Clinics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="resource-card">
            <h4>Education</h4>
            <ul>
                <li>Know Your Constitution</li>
                <li>Rights education programs</li>
                <li>Community legal centers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("*This information is for educational purposes only and does not constitute legal advice. Always consult with a qualified attorney for specific legal matters.*")

# This allows the module to be run independently for testing
if __name__ == "__main__":
    run()
