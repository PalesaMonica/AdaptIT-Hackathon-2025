# pages/property_assistance.py
import streamlit as st
import pandas as pd
import sqlite3
import os
import tempfile
import logging
import traceback
from datetime import datetime

# Configure basic logging (Streamlit captures stderr/stdout)
logging.basicConfig(level=logging.INFO)

# --- Helpers to pick a writable location ---
def find_writable_dir():
    candidates = [
        os.getenv("STREAMLIT_TMP_DIR"),
        os.getenv("TMPDIR"),
        os.getenv("TEMP"),
        os.getenv("TMP"),
        "/tmp",
        os.getcwd(),
        os.path.expanduser("~"),
    ]
    for d in candidates:
        if not d:
            continue
        try:
            os.makedirs(d, exist_ok=True)
            testfile = os.path.join(d, ".write_test")
            with open(testfile, "w") as f:
                f.write("ok")
            os.remove(testfile)
            return d
        except Exception:
            continue
    # final fallback: system temp
    try:
        system_tmp = tempfile.gettempdir()
        os.makedirs(system_tmp, exist_ok=True)
        return system_tmp
    except Exception:
        return None

WRITABLE_DIR = find_writable_dir()
if WRITABLE_DIR:
    DB_PATH = os.path.join(WRITABLE_DIR, "property_queries.db")
    UPLOADS_DIR = os.path.join(WRITABLE_DIR, "uploaded_documents")
else:
    # If absolutely nothing writable, fall back to in-memory DB and no file uploads
    DB_PATH = ":memory:"
    UPLOADS_DIR = None

def log_and_show_exception(e, context=""):
    logging.exception(f"{context}: {e}")
    tb = traceback.format_exc()
    logging.error(tb)
    st.error(f"An internal error occurred. Check app logs for details. ({context})")

# --- Database functions ---
def get_connection():
    try:
        # check_same_thread=False helps when Streamlit spawns multiple worker threads
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        return conn
    except Exception as e:
        logging.exception("Failed to open SQLite connection")
        raise

def init_db():
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS queries (
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
        log_and_show_exception(e, "init_db")

def insert_query(data):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            INSERT INTO queries
            (timestamp, name, email, phone, query_type, urgency, description, files, marketing_consent, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["Timestamp"], data["Name"], data["Email"], data["Phone"], data["Query_Type"],
            data["Urgency"], data["Description"], data["Files"], data["Marketing_Consent"], data["Status"]
        ))
        conn.commit()
        conn.close()
        logging.info("Inserted new query into DB")
    except Exception as e:
        log_and_show_exception(e, "insert_query")
        raise

def fetch_queries():
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM queries ORDER BY id DESC", conn)
        conn.close()
        # ensure column names are consistent (lowercase)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logging.exception("fetch_queries failed")
        # Return empty DataFrame with expected columns to avoid further errors in UI
        cols = ['id','timestamp','name','email','phone','query_type','urgency','description','files','marketing_consent','status']
        return pd.DataFrame(columns=cols)

# --- File saving (uploads) ---
def save_uploaded_file(uploaded_file):
    if not UPLOADS_DIR:
        # Not possible to save uploaded files on this host
        return None, "uploads_not_supported"
    try:
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(UPLOADS_DIR, safe_name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        logging.info(f"Saved uploaded file to {file_path}")
        return file_path, None
    except Exception as e:
        logging.exception("Failed to save uploaded file")
        return None, str(e)

# --- Streamlit UI ---
def run():
    # initialize DB (safe to call repeatedly)
    try:
        init_db()
    except Exception:
        # init_db already logs and shows error
        pass

    # Basic CSS (kept from your original)
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

    st.markdown("""
    <div class="property-header">
        <h1>🏡 Property & Legal Assistance</h1>
        <p style="font-size: 1.1em; opacity: 0.9;">Get professional help with property matters, legal queries, and document assistance</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        with st.form(key="property_form", clear_on_submit=True):
            st.markdown("### 👤 Personal Information")
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            col_email, col_phone = st.columns(2)
            with col_email:
                email = st.text_input("Email Address *", placeholder="your.email@example.com")
            with col_phone:
                phone = st.text_input("Phone Number", placeholder="+27 XX XXX XXXX")

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
                ]
            )

            urgency = st.radio(
                "Urgency Level",
                ["🟢 Normal (7-14 days)", "🟡 Urgent (3-7 days)", "🔴 Very Urgent (24-48 hours)"],
            )

            description = st.text_area("Detailed Description *", height=150)

            uploaded_files = st.file_uploader(
                "Upload relevant documents (optional)",
                type=["pdf", "docx", "doc", "jpg", "jpeg", "png"],
                accept_multiple_files=True,
            )

            privacy_agreed = st.checkbox("I agree to the privacy policy and terms of service")
            marketing_consent = st.checkbox("I consent to receive follow-up communications about my query")

            submit_button = st.form_submit_button("Submit Query 📤")

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
                    # Save uploaded files (if possible) and collect saved filenames
                    uploaded_file_names = []
                    if uploaded_files:
                        for uploaded_file in uploaded_files:
                            try:
                                saved_path, save_err = save_uploaded_file(uploaded_file)
                                if saved_path:
                                    uploaded_file_names.append(os.path.basename(saved_path))
                                else:
                                    # store original name but note error
                                    uploaded_file_names.append(f"{uploaded_file.name} (not saved: {save_err})")
                            except Exception as e:
                                logging.exception("Error while handling uploaded file")
                                uploaded_file_names.append(f"{uploaded_file.name} (error)")

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

                    try:
                        insert_query(query_data)
                        st.markdown(f"""
                        <div class="success-card">
                            <h3 style="color: #059669; margin-top: 0;">✅ Query Submitted Successfully!</h3>
                            <p><strong>Query ID:</strong> QRY_{datetime.now().strftime("%Y%m%d%H%M%S")}</p>
                            <p>📧 You'll receive a confirmation email within 24 hours.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        # rerun to reset form and show admin if needed
                        st.experimental_rerun()
                    except Exception as e:
                        log_and_show_exception(e, "submitting query")
        st.markdown('</div>', unsafe_allow_html=True)

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
            <p><small>This platform connects you with legal professionals but does not provide legal advice directly.</small></p>
        </div>
        """, unsafe_allow_html=True)

        # Admin dashboard
        try:
            if st.checkbox("🔧 Admin: View Previous Queries"):
                df = fetch_queries()
                if len(df) > 0:
                    st.markdown("### 📊 Query Dashboard")
                    col_stats1, col_stats2, col_stats3 = st.columns(3)
                    with col_stats1:
                        st.metric("Total Queries", len(df))
                    with col_stats2:
                        pending = len(df[df['status'] == 'Pending Review']) if 'status' in df.columns else 0
                        st.metric("Pending", pending)
                    with col_stats3:
                        property_queries = len(df[df['query_type'].str.contains('Property', na=False)]) if 'query_type' in df.columns else 0
                        st.metric("Property Queries", property_queries)

                    display_cols = [c for c in ['timestamp', 'query_type', 'urgency', 'status'] if c in df.columns]
                    if display_cols:
                        st.dataframe(df[display_cols].head(10), use_container_width=True)

                    if 'description' in df.columns:
                        st.markdown("**Recent Descriptions:**")
                        for desc in df['description'].head(5).tolist():
                            preview = desc[:100] + "..." if len(desc) > 100 else desc
                            st.write(f"• {preview}")

                    csv_download = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download All Queries (CSV)",
                        data=csv_download,
                        file_name=f"property_queries_full_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("📝 No queries yet.")
        except Exception as e:
            log_and_show_exception(e, "admin dashboard")

if __name__ == "__main__":
    run()
