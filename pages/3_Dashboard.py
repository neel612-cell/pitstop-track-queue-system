import streamlit as st
import qrcode

from io import BytesIO

from streamlit_autorefresh import st_autorefresh
from queue_manager import (
    get_people_ahead,
    get_rider_status,
    get_queue_window,
     get_rider_by_token
)
from database import (
    get_notifications
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏁",
    layout="wide"
)

st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)

# ==========================================
# PROTECTION
# ==========================================

if "token" not in st.session_state:

    st.error(
        "Please register before accessing the dashboard."
    )

    st.page_link(
        "pages/1_Register.py",
        label="Go To Registration"
    )

    st.stop()

# ==========================================
# DATA
# ==========================================

name = st.session_state.get(
    "name",
    "Guest"
)

phone = st.session_state.get(
    "phone",
    "-"
)

token = st.session_state.get(
    "token",
    "-"
)

rider = get_rider_by_token(token)

rider_id = rider[0]

unique_id = st.session_state.get(
    "unique_id",
    "-"
)

people_ahead = get_people_ahead(token)

status = get_rider_status(token)

queue_window = get_queue_window(token)

estimated_wait = people_ahead * 10

total_active = max(len(queue_window), 1)

position = people_ahead + 1

progress = max(
    0,
    min(
        100,
        ((total_active - people_ahead) / total_active) * 100
    )
)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
# PITSTOP

### Race Control
""")

# ==========================================
# ANALYTICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "People Ahead",
        people_ahead
    )

with col2:
    st.metric(
        "Your Token",
        token
    )

with col3:
    st.metric(
        "Estimated Wait",
        f"{estimated_wait} min"
    )

with col4:
    st.metric(
    "Progress",
    f"{progress:.0f}%"
)

# ==========================================
# PROGRESS BAR
# ==========================================

st.progress(
    progress / 100
)

# ==========================================
# RIDER DETAILS
# ==========================================

st.divider()

st.subheader(
    f"Welcome, {name.title()}"
)

left, right = st.columns(2)

with left:

    st.markdown(f"""
    <div style="
        background:#2A2A2A;
        padding:20px;
        border-radius:12px;
        border-left:5px solid #E60000;
    ">
        <h4 style="margin:0;color:#FFE000;">TOKEN</h4>
        <p style="font-size:24px;margin:10px 0;">{token}</p>
        <p style="color:#CCCCCC;">{unique_id}</p>
    </div>
    """, unsafe_allow_html=True)

with right:

    st.markdown(f"""
    <div style="
        background:#2A2A2A;
        padding:20px;
        border-radius:12px;
        border-left:5px solid #FFE000;
    ">
        <h4 style="margin:0;color:#FFE000;">STATUS</h4>
        <p style="font-size:24px;margin:10px 0;">{status}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# LIVE STATUS
# ==========================================

st.divider()

st.subheader(
    "Live Queue Status"
)

st.markdown("### Queue Timeline")

timeline = ""

for rider_token, rider_status in queue_window:

    if rider_status == "On Track":
        timeline += f" 🟢 {rider_token} "

    elif rider_status == "Completed":
        timeline += f" ✅ {rider_token} "

    elif rider_status == "Skipped":
        timeline += f" ⏭️ {rider_token} "

    elif rider_token == token:
        timeline += f" 🔴 **{rider_token}** "

    else:
        timeline += f" ⚪ {rider_token} "

st.markdown(timeline)

if status == "Waiting":

    st.warning(
        "Waiting For Track Assignment"
    )

elif status == "On Track":

    st.success(
        "You Are Currently On Track"
    )

elif status == "Completed":

    st.success(
        "Session Completed"
    )

elif status == "Skipped":

    st.error(
        "You Were Marked As Skipped"
    )

else:

    st.info(status)

# ==========================================
# QR PASS
# ==========================================

st.divider()

if st.button("Show QR Pass"):

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(unique_id)

    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    buffer = BytesIO()

    img.save(
        buffer,
        format="PNG"
    )

    st.image(
        buffer.getvalue(),
        caption=unique_id
    )

# ==========================================
# RECENT UPDATES
# ==========================================

st.divider()

st.subheader(
    "Notifications"
)

notifications = get_notifications(
    rider_id
)

if len(notifications) == 0:

    st.info(
        "No notifications yet."
    )

else:

    for note in notifications:

        st.write(
            f"🔔 {note[1]} | {note[0]}"
        )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "PitStop Track Queue System © 2026"
)
