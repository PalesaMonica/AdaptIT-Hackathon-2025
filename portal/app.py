# app.py
import streamlit as st
from pages import ai_assistance, appointments, tracking, ussd, documents,home
from gtts import gTTS
import tempfile

st.set_page_config(
    page_title="SASSA Portal",
    layout="wide"
)

# ------------------- Pages -------------------
pages = {
    "Home": [st.Page("pages/home.py",title="Home")],
    "Application": [
        st.Page("pages/ai_assistance.py", title="AI Assistance Form"),
        st.Page("pages/tracking.py", title="Track Application")
    ],
    "Services": [
        st.Page("pages/appointments.py", title="Booking"),
        st.Page("pages/ussd.py", title="USSD Demo"),
        st.Page("pages/documents.py", title="Download Document")
    ]
}


selected_page = st.navigation(pages)

# ------------------- Other Pages -------------------
if selected_page.title== "Home":
    home.run()
elif selected_page.title == "AI Assistance Form":
    ai_assistance.run()
elif selected_page.title == "Track Application":
    tracking.run()
elif selected_page.title == "Booking":
    appointments.run()
elif selected_page.title == "USSD Demo":
    ussd.run()
elif selected_page.title == "Download Document":
    documents.run()
