import streamlit as st
from database import initialize_database

initialize_database()

st.set_page_config(
    page_title="Pitstop Track Queue System",
    page_icon="🏁",
    layout="wide"
)

st.title("🏁 Pitstop Track Queue System")

st.success("System Ready")
