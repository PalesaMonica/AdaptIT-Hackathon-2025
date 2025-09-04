# property_assistance.py

import os
import sqlite3
import streamlit as st
from datetime import datetime
import traceback
import logging

# ---------------------------
# Database setup
# ---------------------------

DB_PATH = "/tmp/property_queries.db"
UPLOAD_DIR = "/tmp/uploaded_documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_db():
    """Initialize SQLite database in /tmp"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
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
        logging.info(f"Database initialized at {DB_PATH}")
    except Exception as e:
        logging.error(f"DB init failed: {e}")
        raise

def save_query(data):
    """Insert a query record into the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO property_queries
            (timestamp, name, email, phone, query_type, urgency, description, files, marketing_consent, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["Timestamp"],
            data["Name"],
            data["Email"],
            data["Phone"],
            data["Query_Type"],
            data["Urgency"],
            data["Description"],
            data["Files"],
            data["Marketing_Consent"],
            data["Status"]
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Failed to save query: {e}")
        raise

def load_queries():
    """Load all queries from DB as DataFrame"""
    import pandas as pd
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM property_queries", conn)
        conn.close()
        return df
    except Exception as e:
        logging.error(f"Failed to load queries: {e}")
        return None

# ---------------------------
# Streamlit UI
# ---------------------------

def run():
    try:
        init_db()

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
            uploaded_files = st.file_uploader(
                "Upload relevant documents", accept_multiple_files=True
            )

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
                    # Handle file uploads
                    file_names = []
                    if uploaded_files:
                        for f in uploaded_files:
                            safe_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{f.name}"
                            path = os.path.join(UPLOAD_DIR, safe_name)
                            with open(path, "wb") as out:
                                out.write(f.getbuffer())
                            file_names.append(safe_name)

                    # Prepare query data
                    query_data = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Name": name.strip(),
                        "Email": email.strip(),
                        "Phone": phone.strip() if phone else "Not provided",
                        "Query_Type": query_type,
                        "Urgency": urgency,
                        "Description": description.strip(),
                        "Files": ", ".join(file_names) if file_names else "None",
                        "Marketing_Consent": "Yes" if marketing_consent else "No",
                        "Status": "Pending Review"
                    }

                    save_query(query_data)
                    st.success("✅ Query submitted successfully!")

        # ---------------------------
        # Admin Panel
        # ---------------------------
        if st.checkbox("🔧 Admin: View Previous Queries"):
            df = load_queries()
            if df is not None and not df.empty:
                st.subheader("📊 Recent Queries")
                display_cols = ["timestamp", "query_type", "urgency", "status"]
                st.dataframe(df[display_cols].tail(10), use_container_width=True)
            else:
                st.info("No queries found.")

    except Exception as e:
        st.error(f"⚠️ An unexpected error occurred: {e}")
        st.text(traceback.format_exc())

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    run()
