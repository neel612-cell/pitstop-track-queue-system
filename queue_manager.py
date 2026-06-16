from datetime import datetime
from database import get_connection
from config import (
    TOKEN_PREFIX,
    TOKEN_DIGITS,
    STARTING_TOKEN,
    STATUS_WAITING,
    UNIQUE_ID_PREFIX
)

# ==========================================
# TOKEN GENERATION
# ==========================================

def generate_token():

    today = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT token
    FROM riders
    WHERE queue_date = ?
    ORDER BY id DESC
    LIMIT 1
    """, (today,))

    result = cursor.fetchone()

    conn.close()

    if result is None:
        number = STARTING_TOKEN
    else:
        number = int(
            result[0].replace(TOKEN_PREFIX, "")
        ) + 1

    return f"{TOKEN_PREFIX}{number:0{TOKEN_DIGITS}d}"


# ==========================================
# UNIQUE RIDER ID
# ==========================================

def generate_unique_id():

    year = datetime.now().year

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM riders
    """)

    count = cursor.fetchone()[0] + 1

    conn.close()

    return f"{UNIQUE_ID_PREFIX}-{year}-{count:05d}"


# ==========================================
# REGISTER RIDER
# ==========================================

def register_rider(name, phone):

    token = generate_token()

    unique_id = generate_unique_id()

    registration_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    queue_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM riders
    WHERE phone = ?
    """, (phone,))

    existing = cursor.fetchone()

    if existing:

        conn.close()

        return None, None

    cursor.execute("""
    INSERT INTO riders (
        unique_id,
        token,
        name,
        phone,
        registration_time,
        queue_date,
        status,
        otp_verified,
        terms_accepted
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        unique_id,
        token,
        name,
        phone,
        registration_time,
        queue_date,
        STATUS_WAITING,
        1,
        1
    ))

    conn.commit()
    conn.close()

    return token, unique_id

# ==========================================
# ANALYTICS
# ==========================================

def get_total_riders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM riders
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ==========================================
# PEOPLE AHEAD
# ==========================================

def get_people_ahead(token):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM riders
    WHERE token = ?
    """, (token,))

    current = cursor.fetchone()

    if current is None:
        conn.close()
        return 0

    current_id = current[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM riders
    WHERE id < ?
    AND status IN ('Waiting')
    """, (current_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ==========================================
# PHONE VALIDATION
# ==========================================

def validate_phone(phone):

    if not phone.isdigit():
        return False

    if len(phone) != 10:
        return False

    return True


# ==========================================
# GET RIDER BY TOKEN
# ==========================================

def get_rider_by_token(token):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM riders
    WHERE token = ?
    """, (token,))

    rider = cursor.fetchone()

    conn.close()

    return rider
    
# ==========================================
# GET RIDER STATUS
# ==========================================

def get_rider_status(token):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT status
    FROM riders
    WHERE token = ?
    """, (token,))

    result = cursor.fetchone()

    conn.close()

    if result:

        return result[0]

    return "Unknown"    


# ==========================================
# QUEUE WINDOW
# ==========================================

def get_queue_window(token):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM riders
    WHERE token = ?
    """, (token,))

    current = cursor.fetchone()

    if not current:

        conn.close()
        return []

    current_id = current[0]

    cursor.execute("""
    SELECT token, status
    FROM riders
    WHERE id BETWEEN ? AND ?
    ORDER BY id ASC
    """, (
        current_id - 5,
        current_id + 3
    ))

    result = cursor.fetchall()

    conn.close()

    return result
