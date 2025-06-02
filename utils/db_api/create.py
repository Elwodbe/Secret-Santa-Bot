import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            fullname TEXT,
            registrated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            language VARCHAR(3)
        )
    """)

    conn.commit()
    conn.close()

# Funksiyani chaqiramiz
create_table()
