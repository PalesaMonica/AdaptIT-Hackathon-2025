# property_assistance.py - Property & Legal Help Page
import streamlit as st
import pandas as pd
import os

# Path to store submissions
DATA_FILE = "property_queries.csv"

def run():
    st.title("🏡 Property & Legal Help")
    st.write("Submit your property-related queries and documents to get guidance from verified legal professionals.")

    st.info("⚖️ This tool provides educational guidance and does not replace professional legal advice.")

    # Ensure data file exists
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=["Name", "Email", "Query Type", "Description", "Document"]).to_csv(DATA_FILE, index=False)

    # Property Query Form
    with st.form("property_query_form"):
        st.subheader("Submit Your Property Query")
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        query_type = st.selectbox(
            "Query Type",
            ["Buying Property", "Selling Property", "Rental Issues", "Property Fraud", "Other"]
        )
        description = st.text_area("Describe your issue in detail")
        document = st.file_uploader("Upload Relevant Document (Optional)", type=["pdf", "docx", "jpg", "png"])
        submit_btn = st.form_submit_button("Submit Query")

        if submit_btn:
            # Save uploaded document
            document_path = ""
            if document:
                doc_dir = "uploaded_documents"
                os.makedirs(doc_dir, exist_ok=True)
                document_path = os.path.join(doc_dir, document.name)
                with open(document_path, "wb") as f:
                    f.write(document.getbuffer())

            # Save submission to CSV
            submission = pd.DataFrame([{
                "Name": name,
                "Email": email,
                "Query Type": query_type,
                "Description": description,
                "Document": document_path
            }])
            submission.to_csv(DATA_FILE, mode="a", header=False, index=False)

            st.success("✅ Your query has been submitted successfully!")
            st.write("We will get back to you at:", email)

    # Educational Section
    st.subheader("Property Law Tips & Resources")
    st.markdown("""
    - Always verify the title deed before buying a property.
    - Know tenant and landlord rights under the Rental Housing Act.
    - Beware of property fraud—never pay without confirming ownership.
    - Understand eviction laws to protect tenants and landlords.
    """)
