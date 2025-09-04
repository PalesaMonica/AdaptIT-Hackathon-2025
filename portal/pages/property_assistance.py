# pages/property_assistance.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

def run():
    # Custom CSS styling
    st.markdown("""
    <style>
    .property-header {
        background: linear-gradient(135deg, #10B981, #059669);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .form-container {
        background: linear-gradient(135deg, #F0FDF4, #DCFCE7);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #BBF7D0;
    }
    .info-card {
        background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3B82F6;
        margin: 1rem 0;
    }
    .success-card {
        background: linear-gradient(135deg, #F0FDF4, #DCFCE7);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
        border: none;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #059669, #047857);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
    }
    .query-type-info {
        background: #FEF3C7;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #F59E0B;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="property-header">
        <h1>🏡 Property & Legal Assistance</h1>
        <p style="font-size: 1.1em; opacity: 0.9;">Get professional help with property matters, legal queries, and document assistance</p>
    </div>
    """, unsafe_allow_html=True)

    # Main content in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Query submission form
        with st.form(key="property_form", clear_on_submit=True):
            st.markdown("### 👤 Personal Information")
            
            name = st.text_input(
                "Full Name *", 
                placeholder="Enter your full name",
                help="Your full name as it appears on legal documents"
            )
            
            col_email, col_phone = st.columns(2)
            with col_email:
                email = st.text_input(
                    "Email Address *", 
                    placeholder="your.email@example.com",
                    help="We'll send updates to this email"
                )
            with col_phone:
                phone = st.text_input(
                    "Phone Number", 
                    placeholder="+27 XX XXX XXXX",
                    help="Optional: For urgent queries"
                )
            
            st.markdown("### 📋 Query Information")
            
            query_type = st.selectbox(
                "Type of Assistance Needed *",
                [
                    "Select query type...",
                    "🏠 Property Purchase/Sale",
                    "📄 Property Documentation", 
                    "⚖️ Property Disputes",
                    "🏢 Rental/Lease Issues",
                    "📜 Contract Review",
                    "👨‍⚖️ General Legal Advice",
                    "🏛️ Estate Planning",
                    "💼 Business Legal Matters",
                    "🔧 Other Legal Issue"
                ],
                help="Select the category that best describes your query"
            )
            
            # Show info based on query type
            if query_type and query_type != "Select query type...":
                query_info = {
                    "🏠 Property Purchase/Sale": "Assistance with buying or selling property, transfer processes, and documentation.",
                    "📄 Property Documentation": "Help with property documents, title deeds, and registration.",
                    "⚖️ Property Disputes": "Mediation and legal advice for property-related conflicts.",
                    "🏢 Rental/Lease Issues": "Tenant/landlord disputes, lease agreements, and rental law.",
                    "📜 Contract Review": "Professional review of contracts and legal documents.",
                    "👨‍⚖️ General Legal Advice": "General legal consultation on various matters.",
                    "🏛️ Estate Planning": "Wills, trusts, and estate planning assistance.",
                    "💼 Business Legal Matters": "Business formation, contracts, and commercial law.",
                    "🔧 Other Legal Issue": "Any other legal matter not listed above."
                }
                
                if query_type in query_info:
                    st.markdown(f'<div class="query-type-info">ℹ️ {query_info[query_type]}</div>', 
                              unsafe_allow_html=True)
            
            urgency = st.radio(
                "Urgency Level",
                ["🟢 Normal (7-14 days)", "🟡 Urgent (3-7 days)", "🔴 Very Urgent (24-48 hours)"],
                help="This helps us prioritize your query appropriately"
            )
            
            description = st.text_area(
                "Detailed Description *",
                placeholder="Please provide a detailed description of your query, including relevant background information, specific questions, and any urgency factors...",
                height=150,
                help="The more details you provide, the better we can assist you"
            )
            
            # File upload
            st.markdown("### 📎 Supporting Documents")
            uploaded_files = st.file_uploader(
                "Upload relevant documents (optional)",
                type=["pdf", "docx", "doc", "jpg", "jpeg", "png"],
                accept_multiple_files=True,
                help="You can upload contracts, property documents, images, etc."
            )
            
            # Privacy notice
            st.markdown("### 🔒 Privacy & Terms")
            privacy_agreed = st.checkbox(
                "I agree to the privacy policy and terms of service",
                help="Your information will be shared only with verified legal professionals"
            )
            
            marketing_consent = st.checkbox(
                "I consent to receive follow-up communications about my query"
            )
            
            # Submit button
            st.markdown("---")
            submit_button = st.form_submit_button(
                "Submit Query 📤",
                help="Click to submit your query to our legal professionals"
            )
            
            # Form validation and submission
            if submit_button:
                errors = []
                
                if not name or len(name.strip()) < 2:
                    errors.append("Please enter a valid full name")
                if not email or "@" not in email:
                    errors.append("Please enter a valid email address")
                if query_type == "Select query type...":
                    errors.append("Please select a query type")
                if not description or len(description.strip()) < 10:
                    errors.append("Please provide a detailed description (at least 10 characters)")
                if not privacy_agreed:
                    errors.append("Please agree to the privacy policy and terms")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Process file uploads
                    uploaded_file_names = []
                    if uploaded_files:
                        upload_folder = "uploaded_documents"
                        if not os.path.exists(upload_folder):
                            os.makedirs(upload_folder)
                        
                        for uploaded_file in uploaded_files:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            safe_name = f"{timestamp}_{uploaded_file.name}"
                            file_path = os.path.join(upload_folder, safe_name)
                            
                            try:
                                with open(file_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                uploaded_file_names.append(safe_name)
                            except Exception as e:
                                st.warning(f"Could not save file {uploaded_file.name}: {str(e)}")
                    
                    # Save query to CSV
                    query_data = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": name.strip(),
                        "Email": email.strip(),
                        "Phone": phone.strip() if phone else "Not provided",
                        "Query_Type": query_type,
                        "Urgency": urgency,
                        "Description": description.strip(),
                        "Files": ", ".join(uploaded_file_names) if uploaded_file_names else "None",
                        "Marketing_Consent": "Yes" if marketing_consent else "No",
                        "Status": "Pending Review"
                    }
                    
                    df = pd.DataFrame([query_data])
                    
                    csv_file = "property_queries.csv"
                    try:
                        if os.path.exists(csv_file):
                            df.to_csv(csv_file, mode="a", header=False, index=False)
                        else:
                            df.to_csv(csv_file, index=False)
                        
                        # Success message
                        st.markdown("""
                        <div class="success-card">
                            <h3 style="color: #059669; margin-top: 0;">✅ Query Submitted Successfully!</h3>
                            <p><strong>What happens next:</strong></p>
                            <ul>
                                <li>📧 You'll receive a confirmation email within 24 hours</li>
                                <li>👨‍⚖️ A qualified legal professional will review your query and documents</li>
                                <li>📞 You'll be contacted via your preferred method within the specified timeframe</li>
                                <li>📋 If urgent, we'll prioritize your query accordingly</li>
                                <li>📎 Your uploaded documents will be securely reviewed by our legal team</li>
                            </ul>
                            <p><em>Query ID: QRY_{}</em></p>
                        </div>
                        """.format(datetime.now().strftime("%Y%m%d%H%M%S")), unsafe_allow_html=True)
                        
                        # Add a small delay to ensure file is written, then refresh
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error saving query: {str(e)}")
                        st.error("Please try again or contact support.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar information
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>📞 Contact Information</h3>
            <p><strong>Email:</strong> legal@zaportaL.co.za</p>
            <p><strong>Phone:</strong> +27 11 XXX XXXX</p>
            <p><strong>Hours:</strong> Mon-Fri 8AM-5PM</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <h3>⚖️ Legal Disclaimer</h3>
            <p><small>This platform connects you with legal professionals but does not provide legal advice directly. All consultations are subject to professional legal ethics and confidentiality.</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <h3>🎯 Service Areas</h3>
            <ul style="margin: 0.5rem 0;">
                <li>Property Law</li>
                <li>Contract Law</li>
                <li>Family Law</li>
                <li>Estate Planning</li>
                <li>Business Law</li>
                <li>Consumer Rights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Previous queries section (admin view)
        if st.checkbox("🔧 Admin: View Previous Queries", help="For admin use only"):
            csv_file = "property_queries.csv"
            if os.path.exists(csv_file):
                try:
                    # Read with error handling for malformed CSV
                    df = pd.read_csv(csv_file, quoting=1, escapechar='\\', on_bad_lines='skip')
                    
                    # Clean up any remaining issues
                    if len(df) > 0:
                        st.markdown("### 📊 Query Dashboard")
                        
                        # Summary stats
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        with col_stats1:
                            st.metric("Total Queries", len(df))
                        with col_stats2:
                            pending = len(df[df['Status'] == 'Pending Review']) if 'Status' in df.columns else 0
                            st.metric("Pending", pending)
                        with col_stats3:
                            if 'Query_Type' in df.columns:
                                property_queries = len(df[df['Query_Type'].str.contains('Property', na=False)])
                                st.metric("Property Queries", property_queries)
                        
                        # Query type breakdown
                        if 'Query_Type' in df.columns:
                            st.markdown("**Query Types:**")
                            query_counts = df['Query_Type'].value_counts()
                            for query_type, count in query_counts.head(5).items():
                                st.write(f"• {query_type}: {count}")
                        
                        # Recent queries with better display (excluding personal info)
                        st.markdown("**Recent Queries:**")
                        display_columns = []
                        
                        # Select available columns for display (excluding personal info)
                        if 'Timestamp' in df.columns:
                            display_columns.append('Timestamp')
                        if 'Query_Type' in df.columns:
                            display_columns.append('Query_Type')
                        if 'Urgency' in df.columns:
                            display_columns.append('Urgency')
                        if 'Status' in df.columns:
                            display_columns.append('Status')
                        # Note: Excluding Name, Email, Phone for privacy
                        
                        if display_columns:
                            recent_df = df[display_columns].tail(10).copy()
                            # Clean up display names
                            if 'Query_Type' in recent_df.columns:
                                recent_df['Query_Type'] = recent_df['Query_Type'].str.replace(';', ',')
                            
                            st.dataframe(recent_df, use_container_width=True)
                            
                            # Show anonymized description preview
                            if 'Description' in df.columns:
                                st.markdown("**Recent Query Descriptions (Anonymized):**")
                                for i, desc in enumerate(df['Description'].tail(5).tolist(), 1):
                                    cleaned_desc = str(desc).replace(';', ',')
                                    preview = cleaned_desc[:100] + "..." if len(cleaned_desc) > 100 else cleaned_desc
                                    st.write(f"**Query {i}:** {preview}")
                            
                            # Option to download full data (admin only - includes personal info)
                            st.markdown("---")
                            st.markdown("**🔒 Admin Data Export** (includes personal information)")
                            if st.button("📥 Download All Queries (CSV)", help="Full data export for admin use only"):
                                csv_data = df.to_csv(index=False)
                                st.download_button(
                                    label="Download Full CSV (Admin)",
                                    data=csv_data,
                                    file_name=f"property_queries_full_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv"
                                )
                                st.warning("⚠️ This file contains personal information. Handle with care and in compliance with data protection regulations.")
                        else:
                            st.warning("No displayable columns found in the data.")
                    else:
                        st.info("📝 No valid queries found.")
                        
                except Exception as e:
                    st.error(f"Error loading queries: {str(e)}")
                    st.info("💡 The CSV file may be corrupted. You can:")
                    
                    # Option to reset the CSV file
                    col_reset1, col_reset2 = st.columns(2)
                    with col_reset1:
                        if st.button("🔄 Reset Query Database", help="This will delete all previous queries"):
                            try:
                                os.remove(csv_file)
                                st.success("✅ Query database reset successfully!")
                                st.rerun()
                            except Exception as reset_error:
                                st.error(f"Error resetting database: {str(reset_error)}")
                    
                    with col_reset2:
                        if st.button("🔧 Try Manual Fix", help="Attempt to fix the CSV file"):
                            try:
                                # Try to read with different parameters
                                df_fixed = pd.read_csv(csv_file, sep=',', on_bad_lines='skip', engine='python')
                                if len(df_fixed) > 0:
                                    # Save the fixed version
                                    df_fixed.to_csv(csv_file, index=False, quoting=1)
                                    st.success(f"✅ Fixed CSV file! Recovered {len(df_fixed)} queries.")
                                    st.rerun()
                                else:
                                    st.warning("No recoverable data found.")
                            except Exception as fix_error:
                                st.error(f"Manual fix failed: {str(fix_error)}")
            else:
                st.info("📝 No queries submitted yet.")

if __name__ == "__main__":
    run()