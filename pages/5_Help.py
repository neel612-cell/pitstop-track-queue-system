import streamlit as st

st.title("🏁 Help Center")

st.write(
    "Everything you need to know before your race."
)

with st.expander("How do I join the queue?"):
    st.write("""
    Go to the Registration page,
    enter your details,
    verify your phone number,
    accept the Terms & Conditions,
    and generate your token.
    """)

with st.expander("How do I check my queue position?"):
    st.write("""
    Open the Dashboard page.
    Your token, queue position,
    estimated wait time,
    and live timeline are displayed there.
    """)

with st.expander("What do the timeline colors mean?"):
    st.write("""
    🔴 = Your Position

    ⚪ = Waiting Rider

    🟢 = Currently On Track

    ✅ = Session Completed

    ⏭️ = Rider Skipped
    """)

with st.expander("How will I know when it's my turn?"):
    st.write("""
    The system sends a dashboard notification
    when you are called to the track.
    """)

with st.expander("What if I miss my turn?"):
    st.write("""
    The track operator may temporarily
    mark you as skipped.

    You can be restored back into the queue
    by the administrator.
    """)

with st.expander("What is the QR Pass used for?"):
    st.write("""
    Your QR Pass acts as your digital rider ID.

    Present it to track staff when requested.
    """)

with st.expander("Can I register twice?"):
    st.write("""
    No.

    Duplicate phone numbers are blocked
    to ensure fair queue management.
    """)

with st.expander("Who do I contact for support?"):
    st.write("""
    📞 +91 7330971798

    📧 neelhelps@gmail.com
    """)
    