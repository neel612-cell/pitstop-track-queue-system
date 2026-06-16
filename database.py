import sqlite3
from datetime import datetime
from config import DATABASE_NAME


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    return sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ======================================
    # RIDERS TABLE
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS riders (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        unique_id TEXT UNIQUE,

        token TEXT,

        name TEXT,

        phone TEXT,

        registration_time TEXT,

        queue_date TEXT,

        status TEXT,

        otp_verified INTEGER DEFAULT 0,

        terms_accepted INTEGER DEFAULT 0,

        called_time TEXT,

        track_start_time TEXT,

        completion_time TEXT

    )
    """)

    # ======================================
    # ACTIVITY LOGS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        action TEXT,

        timestamp TEXT

    )
    """)

    # ======================================
    # NOTIFICATIONS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        rider_id INTEGER,

        message TEXT,

        timestamp TEXT

    )
    """)

    # ======================================
    # SETTINGS
    # ======================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        available_karts INTEGER

    )
    """)

    cursor.execute("""
    SELECT COUNT(*)
    FROM settings
    """)

    count = cursor.fetchone()[0]

    if count == 0:

        cursor.execute("""
        INSERT INTO settings (
            available_karts
        )
        VALUES (7)
        """)

    conn.commit()
    conn.close()


# ==========================================
# LOGGING
# ==========================================

def add_log(action):

    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    INSERT INTO activity_logs (
        action,
        timestamp
    )
    VALUES (?, ?)
    """, (
        action,
        timestamp
    ))

    conn.commit()
    conn.close()


# ==========================================
# FETCH LOGS
# ==========================================

def get_logs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM activity_logs
    ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    return logs

def add_notification(rider_id, message):

    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    INSERT INTO notifications (
        rider_id,
        message,
        timestamp
    )
    VALUES (?, ?, ?)
    """, (
        rider_id,
        message,
        timestamp
    ))

    conn.commit()
    conn.close()

def get_notifications(rider_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT message, timestamp
    FROM notifications
    WHERE rider_id=?
    ORDER BY id DESC
    LIMIT 10
    """, (rider_id,))

    data = cursor.fetchall()

    conn.close()

    return data