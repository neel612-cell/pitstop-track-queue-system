import streamlit as st
from datetime import datetime
from database import (
    get_connection,
    add_log,
    add_notification
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🏁",
    layout="wide"
)

# ==========================================
# ADMIN PROTECTION
# ==========================================

if not st.session_state.get(
    "admin_logged_in",
    False
):

    st.error(
        "Admin access required."
    )

    st.stop()

# ==========================================
# DATABASE
# ==========================================

conn = get_connection()
cursor = conn.cursor()

# ==========================================
# SETTINGS
# ==========================================

cursor.execute("""
SELECT available_karts
FROM settings
LIMIT 1
""")

available_karts = cursor.fetchone()[0]

# ==========================================
# ACTIONS
# ==========================================

def send_to_track(rider_id):

    cursor.execute("""
    SELECT COUNT(*)
    FROM riders
    WHERE status='On Track'
    """)

    on_track = cursor.fetchone()[0]

    if on_track >= available_karts:

        st.warning(
            f"Track Full ({on_track}/{available_karts})"
        )

        return

    cursor.execute("""
    SELECT token, name
    FROM riders
    WHERE id=?
    """, (rider_id,))

    rider = cursor.fetchone()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    UPDATE riders
    SET
        status='On Track',
        track_start_time=?
    WHERE id=?
    """, (
        current_time,
        rider_id
    ))

    conn.commit()

    add_notification(
        rider_id,
        "Your session is ready. Proceed to pit lane."
    )

    add_log(
        f"{rider[0]} | {rider[1]} sent to track"
    )


def complete_rider(rider_id):

    cursor.execute("""
    SELECT token, name
    FROM riders
    WHERE id=?
    """, (rider_id,))

    rider = cursor.fetchone()

    completion_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    UPDATE riders
    SET
        status='Completed',
        completion_time=?
    WHERE id=?
    """, (
        completion_time,
        rider_id
    ))

    conn.commit()

    add_notification(
        rider_id,
        "Session completed. Thank you for riding."
    )

    add_log(
        f"{rider[0]} | {rider[1]} completed race"
    )


def skip_rider(rider_id):

    cursor.execute("""
    SELECT token, name
    FROM riders
    WHERE id=?
    """, (rider_id,))

    rider = cursor.fetchone()

    cursor.execute("""
    UPDATE riders
    SET status='Skipped'
    WHERE id=?
    """, (rider_id,))

    conn.commit()

    add_notification(
        rider_id,
        "You were temporarily skipped."
    )

    add_log(
        f"{rider[0]} | {rider[1]} skipped"
    )

# ==========================================
# COUNTS
# ==========================================

cursor.execute("""
SELECT COUNT(*)
FROM riders
WHERE status='Waiting'
""")
waiting_count = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM riders
WHERE status='On Track'
""")
on_track_count = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM riders
WHERE status='Completed'
""")
completed_count = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM riders
WHERE status='Skipped'
""")
skipped_count = cursor.fetchone()[0]

# ==========================================
# HEADER
# ==========================================

st.title("🏁 Admin Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "On Track",
    on_track_count
)

c2.metric(
    "Waiting",
    waiting_count
)

c3.metric(
    "Completed",
    completed_count
)

c4.metric(
    "Skipped",
    skipped_count
)

st.divider()

# ==========================================
# TRACK SETTINGS
# ==========================================

st.subheader(
    "Track Settings"
)

new_capacity = st.number_input(
    "Available Karts",
    min_value=1,
    value=int(available_karts)
)

if st.button(
    "Update Capacity"
):

    cursor.execute("""
    UPDATE settings
    SET available_karts=?
    """, (new_capacity,))

    conn.commit()

    add_log(
        f"Track capacity updated to {new_capacity}"
    )

    st.success(
        "Capacity Updated"
    )

    st.rerun()

# ==========================================
# SEARCH RIDER
# ==========================================

st.subheader("Search Rider")

search_term = st.text_input(
    "Search by Token or Name"
)

if search_term:

    cursor.execute("""
    SELECT *
    FROM riders
    WHERE token LIKE ?
    OR name LIKE ?
    ORDER BY id ASC
    """, (
        f"%{search_term}%",
        f"%{search_term}%"
    ))

    results = cursor.fetchall()

    if len(results) == 0:

        st.warning(
            "No rider found."
        )

    else:

        for rider in results:

            st.success(
                f"{rider[2]} | {rider[3]} | {rider[7]}"
            )

st.divider()

# ==========================================
# WAITING QUEUE
# ==========================================

st.subheader(
    "Waiting Queue"
)

cursor.execute("""
SELECT *
FROM riders
WHERE status='Waiting'
ORDER BY id ASC
""")

waiting = cursor.fetchall()

if len(waiting) == 0:

    st.info(
        "No riders waiting."
    )

for rider in waiting:

    rider_id = rider[0]
    token = rider[2]
    name = rider[3]

    col1, col2 = st.columns(
        [4, 1]
    )

    col1.write(
        f"{token} | {name}"
    )

    if col2.button(
        "Send To Track",
        key=f"track_{rider_id}"
    ):

        send_to_track(
            rider_id
        )

        st.rerun()

st.divider()

# ==========================================
# ON TRACK
# ==========================================

st.subheader(
    "On Track"
)

cursor.execute("""
SELECT *
FROM riders
WHERE status='On Track'
ORDER BY id ASC
""")

track = cursor.fetchall()

if len(track) == 0:

    st.info(
        "No riders on track."
    )

for rider in track:

    rider_id = rider[0]
    token = rider[2]
    name = rider[3]

    c1, c2, c3 = st.columns(
        [4, 1, 1]
    )

    c1.write(
        f"{token} | {name}"
    )

    if c2.button(
        "Complete",
        key=f"complete_{rider_id}"
    ):

        complete_rider(
            rider_id
        )

        st.rerun()

    if c3.button(
        "Skip",
        key=f"skip_{rider_id}"
    ):

        skip_rider(
            rider_id
        )

        st.rerun()

st.divider()

# ==========================================
# COMPLETED
# ==========================================

st.subheader(
    "Completed"
)

cursor.execute("""
SELECT *
FROM riders
WHERE status='Completed'
ORDER BY id DESC
""")

completed = cursor.fetchall()

if len(completed) == 0:

    st.info(
        "No completed riders."
    )

for rider in completed:

    st.write(
        f"{rider[2]} | {rider[3]}"
    )

st.divider()

# ==========================================
# SKIPPED
# ==========================================

st.subheader(
    "Skipped"
)

cursor.execute("""
SELECT *
FROM riders
WHERE status='Skipped'
ORDER BY id DESC
""")

skipped = cursor.fetchall()

if len(skipped) == 0:

    st.info(
        "No skipped riders."
    )

for rider in skipped:

    rider_id = rider[0]
    token = rider[2]
    name = rider[3]

    col1, col2 = st.columns([4, 1])

    col1.write(
        f"{token} | {name}"
    )

    if col2.button(
        "Restore",
        key=f"restore_{rider_id}"
    ):

        cursor.execute("""
        UPDATE riders
        SET status='Waiting'
        WHERE id=?
        """, (rider_id,))

        conn.commit()

        add_log(
            f"{token} | {name} restored to waiting queue"
        )

        st.success(
            f"{token} restored"
        )

        st.rerun()

st.divider()

# ==========================================
# DAILY REPORT
# ==========================================

st.divider()

cursor.execute("""
SELECT AVG(
    (
        julianday(track_start_time)
        -
        julianday(registration_time)
    ) * 24 * 60
)
FROM riders
WHERE track_start_time IS NOT NULL
""")

avg_wait = cursor.fetchone()[0]

st.subheader("Daily Report")

if st.button("Generate Daily Report"):

    st.success("Report Generated")

    st.write(f"Available Karts: {available_karts}")

    st.write(f"Waiting Riders: {waiting_count}")

    st.write(f"On Track Riders: {on_track_count}")

    st.write(f"Completed Riders: {completed_count}")

    st.write(f"Skipped Riders: {skipped_count}")

    total_riders = (
        waiting_count
        + on_track_count
        + completed_count
        + skipped_count
    )

    st.metric(
        "Total Riders Today",
        total_riders
    )

    if avg_wait is not None:

        st.metric(
            "Average Wait Time",
            f"{avg_wait:.1f} min"
        )

# ==========================================
# ACTIVITY LOGS
# ==========================================

st.subheader(
    "Activity Logs"
)

cursor.execute("""
SELECT action, timestamp
FROM activity_logs
ORDER BY id DESC
LIMIT 20
""")

logs = cursor.fetchall()

if len(logs) == 0:

    st.info(
        "No activity recorded."
    )

else:

    for log in logs:

        st.write(
            f"{log[1]} | {log[0]}"
        )

conn.close()
