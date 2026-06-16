import streamlit as st
from database import get_connection

st.set_page_config(
    page_title="Rider History",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Rider History")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT
    token,
    name,
    status,
    registration_time,
    track_start_time,
    completion_time
FROM riders
ORDER BY id DESC
""")

riders = cursor.fetchall()

conn.close()

if len(riders) == 0:

    st.info(
        "No rider history available."
    )

else:

    for rider in riders:

        st.write(
            f"""
Token: {rider[0]}

Name: {rider[1]}

Status: {rider[2]}

Registered: {rider[3]}

Track Start: {rider[4]}

Completed: {rider[5]}
"""
        )

        st.divider()
        