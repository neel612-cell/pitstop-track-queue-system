import streamlit as st
from database import initialize_database

# ==========================================
# INITIALIZE DATABASE
# ==========================================

initialize_database()

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PitStop Track Queue System",
    page_icon="🏁",
    layout="wide"
)

# ==========================================
# PREMIUM FERRARI THEME
# ==========================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #1A1A1A;
    color: #F5F5F0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111111;
}

/* Headers */
h1, h2, h3 {
    color: #FFE000 !important;
    font-weight: 700;
}

/* Paragraphs */
p, div, label {
    color: #F5F5F0;
}

/* Buttons */
.stButton > button {
    background-color: #E60000;
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: bold;
    padding: 0.6rem 1rem;
}

.stButton > button:hover {
    background-color: #FFE000;
    color: black;
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: #2A2A2A;
    border-radius: 12px;
    padding: 15px;
}

/* Success boxes */
.stSuccess {
    border-radius: 12px;
}

/* Info boxes */
.stInfo {
    border-radius: 12px;
}

/* Warning boxes */
.stWarning {
    border-radius: 12px;
}

/* Progress Bar */
.stProgress > div > div > div {
    background-color: #E60000;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
# 🏁 PITSTOP

### Real-Time Track Queue Management

Track. Race. Repeat.
""")

st.markdown("""
<div style="
background:#E60000;
padding:15px;
border-radius:10px;
font-weight:bold;
color:white;">
🏁 SYSTEM READY
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# QUICK INFO
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
🏎️ Digital Registration

Quick rider onboarding
""")

with col2:
    st.info("""
📊 Live Queue Tracking

Real-time rider updates
""")

with col3:
    st.info("""
⚡ Operations Dashboard

Track control & analytics
""")

st.divider()

st.markdown("""
### Welcome

PitStop Track Queue System is designed to provide
a seamless racing experience through real-time queue
management, live notifications, digital rider passes,
and operational analytics.

Use the navigation menu on the left to begin.
""")
