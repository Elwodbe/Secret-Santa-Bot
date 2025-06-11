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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roomname TEXT,
            user_id INTEGER,
            invitation_link TEXT DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)


    conn.commit()
    conn.close()


create_table()

