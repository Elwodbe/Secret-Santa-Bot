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

import sqlite3

def create_tables():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roomname TEXT NOT NULL,
            user_id INTEGER,
            invitation_link TEXT DEFAULT NULL,
            is_active INTEGER DEFAULT 1,  
            is_game_started INTEGER DEFAULT 0,  
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

  
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS room_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            gender TEXT CHECK(gender IN ('male', 'female')),
            fullname TEXT,
            username TEXT,
            about_user TEXT,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Jadval(lar) yaratildi!")

if __name__ == "__main__":
    create_tables()



create_table()

