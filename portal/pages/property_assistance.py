# property_assistance.py

import streamlit as st
from datetime import datetime
import traceback
import logging

# ---------------------------
# Session State Management (replaces SQLite)
# ---------------------------

def init_session_state():
    """Initialize session state for storing queries"""
    if 'property_queries' not in st.session_state:
        st.session_state.property_queries = []

def save_query(data):
    """Add a query to session state"""
    try:
        st.session_state.property_queries.append(data)
        logging.info("Property query saved successfully")
    except Exception as e:
        logging.error(f"Failed to save property query: {e}")
        raise

def load_queries():
    """Load all queries from session state"""
    return st.session_state.get('property_queries', [])

# ---------------------------
# Main function that will be called from app.py
# ---------------------------

def run():
    """Main function to run the property assistance page"""
    try:
        init_session_state()

        st.title("🏡 Property & Legal Assistance")

        with st.form("property_form", clear_on_submit=True):
            st.subheader("👤 Personal Information")
            name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number")

            st.subheader("📋 Query Information")
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
                ]
            )
            urgency = st.radio("Urgency Level", ["🟢 Normal", "🟡 Urgent", "🔴 Very Urgent"])
            description = st.text_area("Detailed Description *")

            st.subheader("📎 Supporting Documents")
            st.info("📝 Note: For deployment, please describe your documents instead of uploading files.")
            document_description = st.text_area("Describe your documents (types, contents, etc.)")

            privacy_agreed = st.checkbox("I agree to the privacy policy and terms")
            marketing_consent = st.checkbox("I consent to receive follow-up communications")

            submit = st.form_submit_button("Submit Query 📤")

            if submit:
                errors = []
                if not name.strip():
                    errors.append("Please enter your name")
                if not email.strip() or "@" not in email:
                    errors.append("Please enter a valid email")
                if query_type == "Select query type...":
                    errors.append("Please select a query type")
                if not description.strip():
                    errors.append("Please provide a description")
                if not privacy_agreed:
                    errors.append("You must agree to the privacy policy")

                if errors:
                    for e in errors:
                        st.error(f"❌ {e}")
                else:
                    # Prepare query data
                    query_data = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": name.strip(),
                        "Email": email.strip(),
                        "Phone": phone.strip() if phone else "Not provided",
                        "Query_Type": query_type,
                        "Urgency": urgency,
                        "Description": description.strip(),
                        "Documents": document_description.strip() if document_description else "None described",
                        "Marketing_Consent": "Yes" if marketing_consent else "No",
                        "Status": "Pending Review"
                    }

                    save_query(query_data)
                    st.success("✅ Query submitted successfully!")
                    st.balloons()

        # ---------------------------
        # Admin Panel
        # ---------------------------
        if st.checkbox("🔧 Admin: View Submitted Queries"):
            queries = load_queries()
            if queries:
                st.subheader(f"📊 Recent Queries ({len(queries)} total)")
                
                for i, query in enumerate(reversed(queries[-10:])):  # Show last 10
                    with st.expander(f"{query['Query_Type']} - {query['Name']} ({query['Timestamp']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Email:** {query['Email']}")
                            st.write(f"**Phone:** {query['Phone']}")
                            st.write(f"**Urgency:** {query['Urgency']}")
                        with col2:
                            st.write(f"**Status:** {query['Status']}")
                            st.write(f"**Marketing Consent:** {query['Marketing_Consent']}")
                        
                        st.write(f"**Description:** {query['Description']}")
                        if query['Documents'] != "None described":
                            st.write(f"**Documents:** {query['Documents']}")
            else:
                st.info("No queries submitted yet.")

        # ---------------------------
        # Footer
        # ---------------------------
        st.markdown("---")
        st.markdown("**Note:** This is a demo application. In production, data would be stored securely and documents would be properly handled.")

    except Exception as e:
        st.error(f"⚠️ An unexpected error occurred: {e}")
        if st.checkbox("Show technical details"):
            st.code(traceback.format_exc())

# ---------------------------
# Entry point for direct execution
# ---------------------------
if __name__ == "__main__":
    run()