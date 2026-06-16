import streamlit as st

st.set_page_config(
    page_title="Terms & Conditions",
    page_icon="🏁",
    layout="wide"
)
st.session_state.terms_viewed = True

st.title("TERMS & CONDITIONS")

st.markdown("""
### PITSTOP TRACK OPERATIONS

**Last Updated: 2026**

---

## 1. ELIGIBILITY

- Participants must be at least **12 years of age**.
- Participants must be a minimum height of **56 inches** to operate Senior Karts.
- Participants must provide accurate personal information during registration.
- Pitstop reserves the right to refuse participation if safety requirements are not met.

---

## 2. SAFETY REQUIREMENTS

By participating, you agree to:

- Follow all instructions provided by Pitstop staff and track marshals.
- Wear all required safety equipment, including helmets and protective gear.
- Drive responsibly and avoid reckless, dangerous, or aggressive behaviour.
- Avoid intentional collisions with karts, barriers, equipment, staff, or other participants.
- Immediately report any safety concerns to staff.

**Failure to follow safety instructions may result in removal from the track without refund.**

---

## 3. ASSUMPTION OF RISK

Go-karting is a recreational motorsport activity that carries inherent risks, including but not limited to:

- Collisions with other karts or barriers.
- Loss of vehicle control.
- Physical injury resulting from racing activities.
- Unexpected track conditions.

By participating, you voluntarily assume all risks associated with the activity.

---

## 4. LIABILITY WAIVER

I acknowledge that participation in karting activities is undertaken at my own risk.

I release and discharge Pitstop, its owners, employees, representatives, contractors, and affiliates from liability for any injury, loss, damage, claim, expense, or accident arising from participation in activities conducted at the venue, except where prohibited by applicable law.

---

## 5. MEDICAL FITNESS

Participants confirm that:

- They are physically and mentally fit to participate.
- They are not under the influence of alcohol, drugs, or any substance that may impair judgment or reaction time.
- Any relevant medical condition affecting participation has been disclosed prior to racing.

---

## 6. DAMAGE TO PROPERTY

Participants agree to be responsible for any deliberate or malicious damage caused to:

- Karts
- Track infrastructure
- Equipment
- Venue property
- Other participants

Pitstop reserves the right to recover repair or replacement costs where applicable.

---

## 7. QUEUE MANAGEMENT

- All riders are assigned a digital queue token.
- Queue positions are managed electronically.
- Riders must remain available when their token is called.
- Failure to report when called may result in reassignment to a later slot.
- Track operations may accommodate up to **7 riders simultaneously**.

---

## 8. PARENT / GUARDIAN CONSENT

For participants under 18 years of age:

A parent or legal guardian must review these Terms & Conditions and provide consent before participation.

By approving registration, the parent or guardian confirms they understand the risks associated with karting activities and accept participation on behalf of the minor.

---

## 9. JURISDICTION

Any dispute, claim, or legal proceeding arising from participation at Pitstop shall be subject exclusively to the jurisdiction of courts located in **Hyderabad, India**.

---

## 10. DECLARATION

By selecting **"I Agree"** and registering for a queue token, I confirm that:

- I have read and understood these Terms & Conditions.
- I agree to follow all safety instructions.
- I voluntarily assume the risks associated with participation.
- I accept the liability waiver and release provisions.
- I am eligible to participate under the stated requirements.
- The information provided by me is accurate and complete.

---

### SUPPORT

**Phone:** +91 73309 71798

**Email:** neelhelps@trackqueue.com

---

**PitStop Track Queue System © 2026**
""")
st.divider()

if st.button("✅ I Have Read And Accept The Terms & Conditions"):

    st.session_state.terms_viewed = True

    st.switch_page("pages/1_Register.py")
    