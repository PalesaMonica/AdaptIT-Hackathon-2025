# property_assistance.py

import os
import sqlite3
import logging
import streamlit as st
import traceback

# ---------------------------
# Database initialization
# ---------------------------

def init_db():
    """Initialize SQLite database in /tmp (safe for Streamlit Cloud)."""
    db_path = os.path.join("/tmp", "property_queries.db")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                query TEXT
            )
        """)
        conn.commit()
        conn.close()

        logging.info(f"Database initialized at {db_path}")
        return db_path
    except Exception as e:
        logging.error(f"DB initialization failed: {e}")
        raise


DB_PATH = init_db()


# ---------------------------
# Save query to DB
# ---------------------------

def save_query(name, email, query):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO queries (name, email, query) VALUES (?, ?, ?)",
            (name, email, query),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Failed to save query: {e}")
        raise


# ---------------------------
# Main Streamlit app
# ---------------------------

def run():
    st.title("🏠 Property Assistance Portal")

    st.write("Submit your property-related queries and we’ll assist you.")

    with st.form("property_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        query = st.text_area("Your Query")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name or not email or not query:
                st.warning("⚠️ Please fill in all fields before submitting.")
            else:
                try:
                    save_query(name, email, query)
                    st.success("✅ Your query has been submitted successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to save your query: {e}")
                    st.text(traceback.format_exc())


# ---------------------------
# Debug entry point
# ---------------------------

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("Error running app:", e)
        print(traceback.format_exc())
