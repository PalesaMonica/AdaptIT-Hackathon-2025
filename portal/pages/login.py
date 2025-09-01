# portal/pages/login.py
import streamlit as st

# Dummy credentials (replace with DB in production)
USER_CREDENTIALS = {
    "user1@example.com": "password123",
    "user2@example.com": "securepass"
}

def run():
    st.set_page_config(page_title="Legal Literacy Portal - Login", layout="centered")

    # Apply blue-themed styling
    st.markdown("""
    <style>
        .login-container {
            max-width: 500px;
            margin: auto;
            padding: 3rem;
            border-radius: 10px;
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            color: white;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }
        .login-container h1 {
            text-align: center;
            color: #EFF6FF;
            margin-bottom: 1.5rem;
        }
        .login-container input {
            border-radius: 5px;
            padding: 0.5rem;
            width: 100%;
            margin-bottom: 1rem;
            border: none;
        }
        .login-container button {
            background: #60A5FA;
            color: white;
            font-weight: bold;
            width: 100%;
            padding: 0.75rem;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .login-container button:hover {
            background: #3B82F6;
        }
        .login-container .info-box {
            background: rgba(255,255,255,0.1);
            padding: 1rem;
            border-radius: 5px;
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = ""

    if st.session_state.logged_in:
        st.success(f"✅ Logged in as {st.session_state.user_email}")
        st.info("You can now access all sections of the Legal Literacy Portal.")
        if st.button("Logout"):
            logout()
        return

    # Login form container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("<h1>Legal Literacy Portal</h1>", unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if email in USER_CREDENTIALS and USER_CREDENTIALS[email] == password:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success(f"Welcome, {email}!")
        else:
            st.error("❌ Invalid email or password. Please try again.")
            st.markdown('<div class="info-box">If you do not have an account, please contact the portal administrator.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.logout()
