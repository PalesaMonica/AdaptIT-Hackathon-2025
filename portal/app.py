# app.py
import streamlit as st

# Import your page modules
from pages import summarizer, fraud_checker, property_assistance, educational, will_generator, sassa_loan, login


# Show main application
st.set_page_config(
    page_title="Legal Literacy Portal",
    layout="wide"
)

# ------------------- Pages -------------------
pages = {
    "Home": [st.Page("pages/home.py", title="Home")],
    "Legal Tools": [
        st.Page("pages/summarizer.py", title="Summarize Legal Documents"),
        st.Page("pages/sassa_loan.py", title="Sassa Loan"),
        st.Page("pages/fraud_checker.py", title="Fraud Detection"),
        st.Page("pages/will_generator.py", title="Will Generator"),
        st.Page("pages/property_assistance.py", title="Property & Lawyer Assistance"),
        st.Page("pages/educational.py", title="Know Your Rights"),
    ]
}

selected_page = st.navigation(pages)

# ------------------- Routing -------------------
if selected_page.title == "Home":
    import pages.home as home
    home.run()

elif selected_page.title == "Summarize Legal Documents":
    summarizer.run()

elif selected_page.title == "Fraud Detection":
    fraud_checker.run()

elif selected_page.title == "Will Generator":
    will_generator.run()

elif selected_page.title == "Property & Lawyer Assistance":
    #property_assistance.run()
    pass

elif selected_page.title == "Know Your Rights":
    educational.run()

elif selected_page.title == "Sassa Loan":
    sassa_loan.run()