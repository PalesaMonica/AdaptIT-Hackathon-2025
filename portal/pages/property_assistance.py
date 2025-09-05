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

def apply_property_styling():
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
    
    /* Elegant Blue-to-Pink Gradient Heading - FIXED SELECTOR */
    .main h1, h1, .stMarkdown h1 {
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
    .main h1::before, h1::before, .stMarkdown h1::before {
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
    
    .main h1::after, h1::after, .stMarkdown h1::after {
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
    
    /* Form section */
    .form-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 3px solid #1E3A8A;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .form-container h2 {
        color: #1E3A8A !important;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Form sections */
    .form-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 5px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .form-section h3 {
        color: #1E3A8A !important;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    
    /* Success card */
    .success-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
        border-left: 6px solid #1E40AF;
    }
    
    /* Info sections */
    .info-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .info-section h3 {
        color: #1E3A8A !important;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    
    /* Terms modal */
    .terms-modal {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 2px solid #1E3A8A;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .terms-modal h4 {
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    
    /* Status tracker */
    .status-tracker {
        display: flex;
        justify-content: space-between;
        margin: 1.5rem 0;
        position: relative;
    }
    
    .status-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        z-index: 2;
    }
    
    .status-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    
    .status-icon.active {
        background: #3B82F6;
        color: white;
    }
    
    .status-icon.completed {
        background: #10B981;
        color: white;
    }
    
    .status-label {
        font-size: 0.8rem;
        text-align: center;
        color: #6B7280;
    }
    
    .status-label.active {
        color: #1E3A8A;
        font-weight: bold;
    }
    
    .status-connector {
        position: absolute;
        top: 20px;
        left: 0;
        right: 0;
        height: 2px;
        background: #e5e7eb;
        z-index: 1;
    }
    
    .status-connector-progress {
        height: 100%;
        background: #10B981;
        transition: width 0.3s ease;
    }
    
    /* Urgency radio styling */
    .stRadio > div {
        flex-direction: row;
        gap: 1rem;
    }
    
    .stRadio > div > label {
        background: #f1f5f9;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border: 2px solid #cbd5e1;
        transition: all 0.3s ease;
        flex: 1;
        text-align: center;
    }
    
    .stRadio > div > label:hover {
        border-color: #1E3A8A;
        background: #e0f2fe;
    }
    
    .stRadio > div > label[data-testid="stRadio"] > div:first-child {
        display: none;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: white !important;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border: none !important;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #1E40AF 0%, #2563EB 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
    }
    
    /* Form elements */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 2px solid #1E3A8A;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        font-weight: 600;
        color: #1E3A8A;
    }
    
    /* File uploader styling */
    .stFileUploader > section {
        border: 2px dashed #1E3A8A;
        border-radius: 8px;
        padding: 1rem;
        background: #f8fafc;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main h1, h1, .stMarkdown h1 {
            font-size: 2.5rem !important;
        }
        
        .form-container {
            padding: 1.5rem;
        }
        
        .stRadio > div {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .status-tracker {
            flex-direction: column;
            gap: 1rem;
        }
        
        .status-connector {
            display: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def show_success_card(query_data):
    """Display a nicely formatted success card with full info."""
    st.markdown(
        f"""
        <div class="success-card">
            <h3>✅ Query Submitted Successfully!</h3>
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
            <p style="font-size:13px; color:#e0f2fe;">Query ID: {query_data['Query_ID']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def show_status_tracker(status="Submitted"):
    """Display a status tracker showing the progress of the query"""
    statuses = ["Submitted", "Under Review", "In Progress", "Resolved"]
    current_index = statuses.index(status) if status in statuses else 0
    
    st.markdown("""
    <div class="status-tracker">
        <div class="status-connector"><div class="status-connector-progress" style="width: {}%;"></div></div>
    """.format((current_index / (len(statuses) - 1)) * 100), unsafe_allow_html=True)
    
    for i, status_name in enumerate(statuses):
        status_class = ""
        if i < current_index:
            status_class = "completed"
        elif i == current_index:
            status_class = "active"
            
        st.markdown(f"""
        <div class="status-step">
            <div class="status-icon {status_class}">{i+1}</div>
            <div class="status-label {status_class if i == current_index else ''}">{status_name}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_terms_modal():
    """Display terms and conditions in an expandable section"""
    with st.expander("📄 Read Terms and Conditions", expanded=False):
        st.markdown("### Property & Legal Assistance Service Terms")
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y')}")
        
        st.markdown("#### 1. Service Description")
        st.markdown("Our Property & Legal Assistance service connects you with qualified professionals who can provide guidance on property and legal matters. This service is designed to offer preliminary advice and direction.")
        
        st.markdown("#### 2. Information Collection")
        st.markdown("We collect personal information including your name, contact details, and information about your property or legal matter to facilitate connecting you with appropriate professionals.")
        
        st.markdown("#### 3. Data Protection")
        st.markdown("Your information is stored securely and only shared with professionals who need it to provide you with assistance. We implement industry-standard security measures to protect your data.")
        
        st.markdown("#### 4. Limitations of Service")
        st.markdown("This service provides initial guidance and does not constitute formal legal representation. For complex legal matters, we recommend engaging a qualified attorney directly.")
        
        st.markdown("#### 5. Response Time")
        st.markdown("We aim to respond to all queries within 2 business days. Urgent queries will be prioritized accordingly.")
        
        st.markdown("#### 6. Privacy Commitment")
        st.markdown("We respect your privacy and will not share your information with third parties for marketing purposes without your explicit consent.")
        
        st.markdown("#### 7. Consent to Communication")
        st.markdown("By using this service, you consent to receive communications related to your query via email, phone, or other provided contact methods.")

# ---------------------------
# Main app
# ---------------------------

def run():
    try:
        init_db()
        apply_property_styling()

        # Header with blue-purple gradient - FIXED: Using proper HTML structure
        st.markdown("""
        <div style="text-align: center;">
            <h1>🏡 Property & Legal Assistance</h1>
            <p style="font-size: 1.2rem; color: #64748B;">Expert Guidance for Your Property and Legal Matters</p>
            <p style="font-size: 0.9rem; color: #94A3B8;">Connect with qualified professionals for your property and legal needs</p>
        </div>
        """, unsafe_allow_html=True)

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
                <div class="form-container">
                <h2>Submit Your Query</h2>
                """,
                unsafe_allow_html=True
            )

            with st.form(key=f"property_form_{form_counter}", clear_on_submit=False):
                # Personal Information Section
                st.markdown("""
                <div class="form-section">
                    <h3>Personal Information</h3>
                </div>
                """, unsafe_allow_html=True)
                
                name_col, email_col = st.columns(2)
                with name_col:
                    name = st.text_input("Full Name *", key=f"pa_name_{form_counter}", 
                                        placeholder="Enter your full name")
                with email_col:
                    email = st.text_input("Email Address *", key=f"pa_email_{form_counter}", 
                                         placeholder="your.email@example.com")
                
                phone = st.text_input("Phone Number", key=f"pa_phone_{form_counter}", 
                                     placeholder="+27 123 456 7890")

                # Query Information Section
                st.markdown("""
                <div class="form-section">
                    <h3>Query Information</h3>
                </div>
                """, unsafe_allow_html=True)
                
                query_type = st.selectbox(
                    "Type of Assistance Needed *",
                    [
                        "Select query type...",
                        "Property Purchase/Sale",
                        "Property Documentation",
                        "Property Disputes",
                        "Rental/Lease Issues",
                        "General Legal Advice",
                        "Business Legal Matters",
                        "Other Legal Issue"
                    ],
                    key=f"pa_query_type_{form_counter}"
                )
                
                # Urgency selection using radio buttons (properly styled)
                urgency_options = ["Normal", "Urgent", "Very Urgent"]
                urgency = st.radio(
                    "Urgency Level *",
                    options=urgency_options,
                    key=f"pa_urgency_{form_counter}",
                    horizontal=True
                )
                
                description = st.text_area("Detailed Description *", key=f"pa_description_{form_counter}", 
                                          height=150, placeholder="Please describe your property or legal issue in detail...")

                # Supporting Documents Section
                st.markdown("""
                <div class="form-section">
                    <h3>Supporting Documents</h3>
                </div>
                """, unsafe_allow_html=True)
                
                uploaded_files = st.file_uploader(
                    "Upload relevant documents (PDF, images, text files)",
                    accept_multiple_files=True,
                    key=f"pa_files_{file_counter}",
                    help="Upload any contracts, photos, or documents related to your query"
                )
                
                if uploaded_files:
                    st.success(f"{len(uploaded_files)} file(s) selected for upload")

                # Privacy & Consent Section
                st.markdown("""
                <div class="form-section">
                    <h3>Privacy & Consent</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Terms and conditions
                show_terms_modal()
                
                privacy_col, marketing_col = st.columns(2)
                with privacy_col:
                    privacy_agreed = st.checkbox("I agree to the privacy policy and terms *", 
                                                key=f"pa_privacy_{form_counter}")
                with marketing_col:
                    marketing_consent = st.checkbox("I consent to receive follow-up communications", 
                                                   key=f"pa_marketing_{form_counter}")

                # Submit button (must be inside the form)
                submit = st.form_submit_button("Submit Query", use_container_width=True)

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
                            "Status": "Submitted"
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
                            
                            # Show status tracker
                            st.markdown("""
                            <div class="form-section">
                                <h3>Query Status</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            show_status_tracker("Submitted")
                            
                            # Show success
                            show_success_card(query_data)

            st.markdown("</div>", unsafe_allow_html=True)

        # ---------------------------
        # Right Column: Information & Previous Queries
        # ---------------------------
        with right_col:
            # Information section
            st.markdown("""
            <div class="info-section">
                <h3>How It Works</h3>
                <ol style="line-height:1.7;">
                    <li>Submit your property or legal query</li>
                    <li>Our system reviews your information</li>
                    <li>A qualified professional contacts you</li>
                    <li>Receive personalized guidance</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
            # Response time information
            st.markdown("""
            <div class="info-section">
                <h3>Expected Response Times</h3>
                <ul style="line-height:1.7;">
                    <li><b>Normal queries:</b> 2-3 business days</li>
                    <li><b>Urgent queries:</b> Within 24 hours</li>
                    <li><b>Very urgent:</b> Same day response</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Contact information
            st.markdown("""
            <div class="info-section">
                <h3>Need Immediate Help?</h3>
                <p><b>Phone:</b> 0861 123 456</p>
                <p><b>Email:</b> help@propertylegal.co.za</p>
                <p><b>Hours:</b> Mon-Fri, 8am-5pm</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Previous queries section with status tracking
            show_queries = st.checkbox("View My Previous Queries")
            if show_queries:
                st.markdown("""
                <div class="info-section">
                    <h3>Previous Queries</h3>
                </div>
                """, unsafe_allow_html=True)
                
                df = load_queries()
                if df is not None and not df.empty:
                    # Show status for each query
                    for _, row in df.tail(5).iterrows():
                        with st.expander(f"Query: {row['query_id']} - {row['query_type']}"):
                            st.write(f"**Submitted:** {row['timestamp']}")
                            st.write(f"**Status:** {row.get('status', 'Submitted')}")
                            show_status_tracker(row.get('status', 'Submitted'))
                            st.write(f"**Description:** {row['description'][:100]}...")
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