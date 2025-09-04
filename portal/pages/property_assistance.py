import streamlit as st
import pandas as pd
import os
import sqlite3
from datetime import datetime
import logging

# ✅ Force DB into /tmp (works for both local + deployed runs)
DB_PATH = os.path.join("/tmp", "property_queries.db")

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS property_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            query_type TEXT,
            urgency TEXT,
            description TEXT,
            files TEXT,
            marketing_consent TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()
    logging.info(f"✅ Database initialized at {DB_PATH}")

def save_query(query_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO property_queries 
        (timestamp, name, email, phone, query_type, urgency, description, files, marketing_consent, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        query_data["Timestamp"],
        query_data["Name"],
        query_data["Email"],
        query_data["Phone"],
        query_data["Query_Type"],
        query_data["Urgency"],
        query_data["Description"],
        query_data["Files"],
        query_data["Marketing_Consent"],
        query_data["Status"]
    ))
    conn.commit()
    conn.close()

def load_queries():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM property_queries", conn)
    conn.close()
    return df

def run():
    init_db()

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
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="property-header">
        <h1>🏡 Property & Legal Assistance</h1>
        <p style="font-size: 1.1em; opacity: 0.9;">Get professional help with property matters, legal queries, and document assistance</p>
    </div>
    """, unsafe_allow_html=True)

    # Query submission form
    with st.form(key="property_form", clear_on_submit=True):
        name = st.text_input("Full Name *")
        email = st.text_input("Email Address *")
        phone = st.text_input("Phone Number")
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
        uploaded_files = st.file_uploader("Upload relevant documents", accept_multiple_files=True)

        privacy_agreed = st.checkbox("I agree to the privacy policy and terms")
        marketing_consent = st.checkbox("I consent to receive follow-up communications")

        submit_button = st.form_submit_button("Submit Query 📤")

        if submit_button:
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
                errors.append("Please agree to the privacy policy")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                uploaded_file_names = []
                if uploaded_files:
                    upload_folder = "/tmp/uploaded_documents"
                    os.makedirs(upload_folder, exist_ok=True)
                    for f in uploaded_files:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        safe_name = f"{timestamp}_{f.name}"
                        file_path = os.path.join(upload_folder, safe_name)
                        with open(file_path, "wb") as out:
                            out.write(f.getbuffer())
                        uploaded_file_names.append(safe_name)

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

                save_query(query_data)

                st.success("✅ Query submitted successfully!")

    # Admin panel
    if st.checkbox("🔧 Admin: View Previous Queries"):
        try:
            df = load_queries()
            if not df.empty:
                st.dataframe(df.tail(10), use_container_width=True)
            else:
                st.info("No queries found.")
        except Exception as e:
            st.error(f"Error loading queries: {e}")

if __name__ == "__main__":
    run()
