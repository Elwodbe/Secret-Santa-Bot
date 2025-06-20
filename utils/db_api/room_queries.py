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

def get_room_info(room_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT rooms.id, rooms.roomname, users.username, users.fullname
        FROM rooms
        JOIN users ON rooms.user_id = users.user_id
        WHERE rooms.id = ?
    """, (room_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "room_id": result[0],
            "room_name": result[1],
            "creator_username": result[2],
            "creator_fullname": result[3]
        }
    else:
        return None


def add_user_room(room_id, user_id, gender, fullname, username, about_user):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO room_users (room_id, user_id, gender, fullname, username, about_user)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (room_id, user_id, gender, fullname, username, about_user))

    conn.commit()
    conn.close()

def is_user_in_room(room_id, user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM room_users
        WHERE room_id = ? AND user_id = ?
        LIMIT 1
    """, (room_id, user_id))

    result = cursor.fetchone()

    conn.close()
    return result is not None

import sqlite3

import sqlite3

def get_user_rooms_with_details(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    query = """
    SELECT 
        r.id AS room_id,
        r.roomname,
        r.invitation_link,
        r.is_game_started,
        ru.gender,
        ru.fullname,
        ru.username,
        ru.about_user
    FROM 
        room_users ru
    JOIN 
        rooms r ON ru.room_id = r.id
    WHERE 
        ru.user_id = ?
        AND r.is_active = 1
    """

    try:
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        result = []
        for row in rows:
            room_info = {
                "room_id": row[0],
                "roomname": row[1],
                "invitation_link": row[2],
                "is_game_started": bool(row[3]),
                "gender": row[4],
                "fullname": row[5],
                "username": row[6],
                "about_user": row[7]
            }
            result.append(room_info)

        return result

    except sqlite3.Error as e:
        print("Xatolik yuz berdi:", e)
        return []

    finally:
        conn.close()
