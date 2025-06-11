import sqlite3


def check_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id=? AND is_active = 1", (user_id,))
    user = cursor.fetchone()

    conn.close()

    return user is not None

def add_user(user_id, username, fullname, language='uz'):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT is_active FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result is not None:
        cursor.execute('''
            UPDATE users
            SET is_active = 1,
                language = ?,
                username = ?,
                fullname = ?
            WHERE user_id = ?
        ''', (language, username, fullname, user_id))
    else:
        cursor.execute('''
            INSERT INTO users (user_id, username, fullname, is_active, language)
            VALUES (?, ?, ?, 1, ?)
        ''', (user_id, username, fullname, language))

    conn.commit()
    conn.close()


def  get_user_language(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else False


