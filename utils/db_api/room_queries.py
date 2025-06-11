import sqlite3

def create_room(room_name, user_id):
    conn = sqlite3.connect("database.db") 
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rooms (roomname, user_id)
        VALUES (?, ?)
    """, (room_name, user_id))
    conn.commit()

    room_id = cursor.lastrowid

    invitation_link = f"https://t.me/silisovgaa_bot?start={room_id}"

    cursor.execute("""
        UPDATE rooms
        SET invitation_link = ?
        WHERE id = ?
    """, (invitation_link, room_id))
    conn.commit()
    cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
    room_info = cursor.fetchone()

    conn.close()
    return room_info
