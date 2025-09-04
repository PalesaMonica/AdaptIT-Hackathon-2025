# pages/educational.py - Know Your Rights Module
import streamlit as st

def run():
    """
    Main function called by app.py when "Know Your Rights" page is selected
    """
    
    # Custom CSS for better styling that matches the app theme
    st.markdown("""
    <style>
        .rights-card {
            background: rgba(255, 255, 255, 0.8);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.2);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }
        
        .rights-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
            background: rgba(59, 130, 246, 0.05);
        }
        
        .rights-card-human {
            border-left: 4px solid #3b82f6;
        }
        
        .rights-card-constitutional {
            border-left: 4px solid #8b5cf6;
        }
        
        .rights-card-civil {
            border-left: 4px solid #10b981;
        }
        
        .rights-card-worker {
            border-left: 4px solid #f59e0b;
        }
        
        .rights-card-consumer {
            border-left: 4px solid #06b6d4;
        }
        
        .rights-card-family {
            border-left: 4px solid #ec4899;
        }
        
        .rights-card-digital {
            border-left: 4px solid #6366f1;
        }
        
        .rights-card-legal {
            border-left: 4px solid #ef4444;
        }
        
        .emergency-box {
            background: rgba(239, 68, 68, 0.1);
            border-left: 4px solid #ef4444;
            padding: 1.5rem;
            margin: 2rem 0;
            border-radius: 8px;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        .detail-box {
            background: rgba(255, 255, 255, 0.6);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(59, 130, 246, 0.2);
            margin: 1rem 0;
            backdrop-filter: blur(10px);
        }
        
        .category-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            display: block;
        }
        
        .category-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #1E293B;
            margin-bottom: 0.5rem;
        }
        
        .category-desc {
            font-size: 0.9rem;
            color: #475569;
            line-height: 1.4;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state for this page
    if 'selected_rights_category' not in st.session_state:
        st.session_state.selected_rights_category = None

    # Rights categories data
    rights_categories = {
        'Human Rights': {
            'icon': '👥',
            'description': 'Universal rights inherent to all human beings',
            'examples': ['Right to life', 'Freedom from torture', 'Right to education', 'Freedom of expression'],
            'css_class': 'rights-card-human'
        },
        'Constitutional Rights': {
            'icon': '⚖️',
            'description': 'Rights protected by your constitution',
            'examples': ['Freedom of speech', 'Right to privacy', 'Due process', 'Equal protection'],
            'css_class': 'rights-card-constitutional'
        },
        'Civil Rights': {
            'icon': '🛡️',
            'description': 'Rights to participate in society without discrimination',
            'examples': ['Anti-discrimination', 'Voting rights', 'Access to public services', 'Fair housing'],
            'css_class': 'rights-card-civil'
        },
        'Worker Rights': {
            'icon': '💼',
            'description': 'Rights in the workplace and employment',
            'examples': ['Fair wages', 'Safe working conditions', 'Right to organize', 'Protection from harassment'],
            'css_class': 'rights-card-worker'
        },
        'Consumer Rights': {
            'icon': '🛒',
            'description': 'Rights when purchasing goods and services',
            'examples': ['Right to refund', 'Product safety', 'Fair pricing', 'Privacy protection'],
            'css_class': 'rights-card-consumer'
        },
        'Family Rights': {
            'icon': '👨‍👩‍👧‍👦',
            'description': 'Rights related to family, marriage, and children',
            'examples': ['Parental rights', 'Child protection', 'Marriage equality', 'Custody rights'],
            'css_class': 'rights-card-family'
        },
        'Digital Rights': {
            'icon': '💻',
            'description': 'Rights in the digital age and online spaces',
            'examples': ['Data privacy', 'Digital access', 'Online freedom', 'Cybersecurity protection'],
            'css_class': 'rights-card-digital'
        },
        'Legal Proceedings': {
            'icon': '⚖️',
            'description': 'Rights when dealing with courts and law enforcement',
            'examples': ['Right to counsel', 'Right to remain silent', 'Fair trial', 'Presumption of innocence'],
            'css_class': 'rights-card-legal'
        }
    }

    # Page header (no need for hero header as that's handled by app.py)
    st.markdown("# 📚 Know Your Rights")
    st.markdown("### Understanding your rights is the foundation of justice. Explore different categories to learn about your legal protections and freedoms.")
    st.markdown("---")

    # Rights categories grid
    if not st.session_state.selected_rights_category:
        st.markdown("## 📋 Rights Categories")
        st.markdown("*Click on any category below to learn more*")
        
        # Create columns for grid layout
        cols = st.columns(2)  # 2 columns for better mobile experience
        
        for i, (category, info) in enumerate(rights_categories.items()):
            with cols[i % 2]:
                # Create custom styled button using markdown and button
                st.markdown(f"""
                <div class="rights-card {info['css_class']}">
                    <span class="category-icon">{info['icon']}</span>
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
            if st.button("← Back", type="secondary"):
                st.session_state.selected_rights_category = None
                st.rerun()
        
        with col_title:
            st.markdown(f"## {info['icon']} {selected}")
        
        st.markdown(f"**{info['description']}**")
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Key Areas Include:")
            for example in info['examples']:
                st.markdown(f"• {example}")
            
            # Add South African context
            st.markdown("### 🇿🇦 In South Africa:")
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
            st.markdown("### 🚀 Quick Actions")
            
            if st.button("📚 Learn the Basics", use_container_width=True):
                st.info("📖 Essential information everyone should know about this area of rights")
            
            if st.button("🎯 Common Scenarios", use_container_width=True):
                st.info("💡 Real-world situations and how to handle them effectively")
            
            if st.button("🆘 Know When to Get Help", use_container_width=True):
                st.info("📞 When to contact a lawyer, legal aid, or advocacy group")
            
            if st.button("🏢 Find Resources", use_container_width=True):
                st.info("🔗 Links to relevant government departments and NGOs")
            
            st.markdown('</div>', unsafe_allow_html=True)

    # Emergency Rights Section - Always visible
    st.markdown("---")
    st.markdown('<div class="emergency-box">', unsafe_allow_html=True)
    st.markdown("### 🚨 Emergency Rights Reminder")
    st.markdown("In any interaction with law enforcement or legal proceedings, remember these fundamental rights:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("• **Right to remain silent** - You don't have to answer questions")
        st.markdown("• **Right to an attorney** - Legal representation is your right")

    with col2:
        st.markdown("• **Refuse searches without warrant** - Unless lawfully required")
        st.markdown("• **Know why you're detained** - Police must inform you")

    st.markdown("**📞 Important Numbers:** Legal Aid SA: 0800 110 110 | Police: 10111 | Emergency: 112")
    st.markdown('</div>', unsafe_allow_html=True)

    # Resources section
    st.markdown("---")
    st.markdown("## 🔗 Helpful Resources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏛️ Government**")
        st.markdown("• Department of Justice")
        st.markdown("• Human Rights Commission")
        st.markdown("• Public Protector")
    
    with col2:
        st.markdown("**⚖️ Legal Aid**")
        st.markdown("• Legal Aid South Africa")
        st.markdown("• ProBono.Org")
        st.markdown("• University Law Clinics")
    
    with col3:
        st.markdown("**📚 Education**")
        st.markdown("• Know Your Constitution")
        st.markdown("• Rights education programs")
        st.markdown("• Community legal centers")

    # Footer
    st.markdown("---")
    st.markdown("*This information is for educational purposes only and does not constitute legal advice. Always consult with a qualified attorney for specific legal matters.*")

# This allows the module to be run independently for testing
if __name__ == "__main__":
    run()