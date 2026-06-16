import streamlit as st

from config import (
    DEMO_OTP,
    ADMIN_TRIGGER,
    ADMIN_USERNAME,
    ADMIN_PASSWORD
)

from queue_manager import (
    register_rider,
    validate_phone
)

# ==========================================
# SESSION STATE
# ==========================================

if "name" not in st.session_state:
    st.session_state.name = ""

if "phone" not in st.session_state:
    st.session_state.phone = ""

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

if "terms_viewed" not in st.session_state:
    st.session_state.terms_viewed = False

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Register",
    page_icon="🏁",
    layout="wide"
)

st.title("🏁 Rider Registration")

st.write(
    "Register for your upcoming track session."
)

# ==========================================
# NAME
# ==========================================

name = st.text_input(
    "Full Name",
    value=st.session_state.name
)

st.session_state.name = name

# ==========================================
# PHONE
# ==========================================

phone = st.text_input(
    "Mobile Number",
    value=st.session_state.phone
)

st.session_state.phone = phone

# ==========================================
# ADMIN PORTAL
# ==========================================

if name.strip().upper() == ADMIN_TRIGGER:

    st.warning("Admin Portal Access")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Admin Login"):

        if (
            username == ADMIN_USERNAME
            and
            password == ADMIN_PASSWORD
        ):

            st.session_state.admin_logged_in = True

            st.success(
                "Admin Login Successful"
            )

            st.switch_page(
                "pages/4_Admin.py"
            )

        else:

            st.error(
                "Invalid Credentials"
            )

    st.stop()

# ==========================================
# OTP VERIFICATION
# ==========================================

st.subheader("OTP Verification")

if st.button("Send OTP"):

    if not validate_phone(phone):

        st.error(
            "Enter a valid 10 digit phone number."
        )

    else:

        st.session_state.otp_sent = True

        st.info(
            f"Demo OTP: {DEMO_OTP}"
        )

if st.session_state.otp_sent:

    otp = st.text_input(
        "Enter OTP",
        max_chars=6
    )

    if st.button("Verify OTP"):

        if otp == DEMO_OTP:

            st.session_state.otp_verified = True

            st.success(
                "OTP Verified Successfully"
            )

        else:

            st.error(
                "Incorrect OTP"
            )

# ==========================================
# TERMS
# ==========================================

st.divider()

st.subheader(
    "Terms & Conditions"
)

st.page_link(
    "pages/2_Terms.py",
    label="Read Terms & Conditions"
)

if not st.session_state.terms_viewed:

    st.warning(
        "Please read the Terms & Conditions before continuing."
    )

    accepted = False

else:

    accepted = st.checkbox(
        "I have read and agree to the Terms & Conditions"
    )

# ==========================================
# REGISTER
# ==========================================

st.divider()

if st.button("Generate My Token"):

    if not name.strip():

        st.error(
            "Please enter your name."
        )

    elif not validate_phone(phone):

        st.error(
            "Enter a valid phone number."
        )

    elif not st.session_state.otp_verified:

        st.error(
            "OTP verification required."
        )

    elif not accepted:

        st.error(
            "Please accept the Terms & Conditions."
        )

    else:

        token, unique_id = register_rider(
            name,
            phone
        )

        if token is None:

            st.error(
                "Phone number already registered."
            )

            st.stop()

        st.session_state.token = token
        st.session_state.unique_id = unique_id

        st.success(
            f"Registration Successful! Token: {token}"
        )

        st.switch_page(
            "pages/3_Dashboard.py"
        )
        