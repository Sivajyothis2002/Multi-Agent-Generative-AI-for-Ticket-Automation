import sqlite3

DB_NAME = "ticket_history.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        body TEXT,
        category TEXT,
        priority TEXT,
        queue TEXT,
        response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_ticket(subject, body, category, priority, queue, response):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history
    (subject, body, category, priority, queue, response)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        subject,
        body,
        category,
        priority,
        queue,
        response
    ))

    conn.commit()
    conn.close()


def get_history():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM history
    ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows