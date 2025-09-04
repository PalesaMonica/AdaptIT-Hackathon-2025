# property_assistance.py

import os
import sqlite3
import streamlit as st
from datetime import datetime
import traceback
import logging

# ---------------------------
# Config / logging
# ---------------------------
DB_PATH = "/tmp/property_queries.db"
UPLOAD_DIR = "/tmp/uploaded_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)

# ---------------------------
# Database helpers
# ---------------------------

def init_db():
    """Ensure table exists and add `query_id` if missing on older DBs."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS property_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id TEXT,
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

        cursor.execute("PRAGMA table_info(property_queries)")
        cols = [row[1] for row in cursor.fetchall()]
        if "query_id" not in cols:
            logging.info("Adding missing column `query_id` to property_queries table.")
            cursor.execute("ALTER TABLE property_queries ADD COLUMN query_id TEXT")
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
            (query_id, timestamp, name, email, phone, query_type, urgency, description, files, marketing_consent, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["Query_ID"],
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
    """Load all queries from DB as DataFrame (returns None on error)"""
    try:
        import pandas as pd
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM property_queries", conn)
        conn.close()
        return df
    except Exception as e:
        logging.error(f"Failed to load queries: {e}")
        return None

# ---------------------------
# UI helpers
# ---------------------------

def show_success_card(query_data):
    """Display a nicely formatted success card with full info."""
    st.markdown(
        f"""
        <div style="max-width:600px; margin:auto; background-color:#e6f7ee; 
                    padding:20px; border-radius:12px; border-left:6px solid #2ecc71;">
            <h3 style="color:#2ecc71; margin-top:0;">✅ Query Submitted Successfully!</h3>
            <p><b>Thank you, {query_data['Name']}!</b></p>
            <p><b>What happens next:</b></p>
            <ul style="line-height:1.7;">
                <li>📧 You'll receive a confirmation email at {query_data['Email']}</li>
                <li>👩‍⚖️ A qualified legal professional will review your query</li>
                <li>📞 Contact via preferred method (phone: {query_data['Phone']})</li>
                <li>📝 If urgent, we'll prioritize your query accordingly</li>
            </ul>
            <p><b>Query Details:</b></p>
            <ul style="line-height:1.5;">
                <li>Type: {query_data['Query_Type']}</li>
                <li>Urgency: {query_data['Urgency']}</li>
                <li>Uploaded Files: {query_data['Files']}</li>
            </ul>
            <p style="font-size:13px; color:#555;">Query ID: {query_data['Query_ID']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# Main app
# ---------------------------

def run():
    try:
        init_db()

        st.title("🏡 Property & Legal Assistance")

        # Initialize counters for form and file uploader
        if "pa_form_counter" not in st.session_state:
            st.session_state["pa_form_counter"] = 0
        if "pa_files_counter" not in st.session_state:
            st.session_state["pa_files_counter"] = 0

        form_counter = st.session_state["pa_form_counter"]
        file_counter = st.session_state["pa_files_counter"]

        # Layout
        left_col, right_col = st.columns([2, 1])

        # ---------------------------
        # Left Column: Form
        # ---------------------------
        with left_col:
            st.markdown(
                """
                <div style="background-color:#ffffff; padding:25px; border-radius:12px; 
                            box-shadow:0 4px 12px rgba(0,0,0,0.06); border:1px solid #eee;">
                """,
                unsafe_allow_html=True
            )

            with st.form(key=f"property_form_{form_counter}", clear_on_submit=False):
                st.subheader("👤 Personal Information")
                name = st.text_input("Full Name *", key=f"pa_name_{form_counter}")
                email = st.text_input("Email Address *", key=f"pa_email_{form_counter}")
                phone = st.text_input("Phone Number", key=f"pa_phone_{form_counter}")

                st.subheader("📋 Query Information")
                query_type = st.selectbox(
                    "Type of Assistance Needed *",
                    [
                        "Select query type...",
                        "🏠 Property Purchase/Sale",
                        "📄 Property Documentation",
                        "⚖️ Property Disputes",
                        "🏢 Rental/Lease Issues",
                        "👨‍⚖️ General Legal Advice",
                        "💼 Business Legal Matters",
                        "🔧 Other Legal Issue"
                    ],
                    key=f"pa_query_type_{form_counter}"
                )
                urgency = st.radio(
                    "Urgency Level",
                    ["🟢 Normal", "🟡 Urgent", "🔴 Very Urgent"],
                    key=f"pa_urgency_{form_counter}"
                )
                description = st.text_area("Detailed Description *", key=f"pa_description_{form_counter}")

                st.subheader("📎 Supporting Documents")
                uploaded_files = st.file_uploader(
                    "Upload relevant documents",
                    accept_multiple_files=True,
                    key=f"pa_files_{file_counter}"
                )

                privacy_agreed = st.checkbox("I agree to the privacy policy and terms", key=f"pa_privacy_{form_counter}")
                marketing_consent = st.checkbox("I consent to receive follow-up communications", key=f"pa_marketing_{form_counter}")

                submit = st.form_submit_button("Submit Query 📤")

                if submit:
                    # Validation
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
                        # Save uploaded files
                        file_names = []
                        if uploaded_files:
                            for f in uploaded_files:
                                safe_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{f.name}"
                                path = os.path.join(UPLOAD_DIR, safe_name)
                                with open(path, "wb") as out:
                                    out.write(f.getbuffer())
                                file_names.append(safe_name)

                        # Generate query data
                        query_id = f"QRY_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                        query_data = {
                            "Query_ID": query_id,
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

                        # Save to DB
                        try:
                            save_query(query_data)
                        except Exception:
                            st.error("⚠️ Failed to save query. See logs for details.")
                            logging.exception("Failed to save query")
                        else:
                            # Increment counters to force form & uploader reset
                            st.session_state["pa_form_counter"] += 1
                            st.session_state["pa_files_counter"] += 1

                            # Show success
                            show_success_card(query_data)

            st.markdown("</div>", unsafe_allow_html=True)

        # ---------------------------
        # Right Column: Previous Queries
        # ---------------------------
        with right_col:
            show_queries = st.checkbox("📂 Show My Previous Queries")
            if show_queries:
                st.subheader("🔧 Previous Queries")
                df = load_queries()
                if df is not None and not df.empty:
                    expected_cols = ["query_id", "timestamp", "query_type", "urgency", "status"]
                    display_cols = [col for col in expected_cols if col in df.columns]
                    if display_cols:
                        st.dataframe(df[display_cols].tail(10), width="stretch")
                    else:
                        st.dataframe(df.tail(10), width="stretch")
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
