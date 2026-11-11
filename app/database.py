import sqlite3
from datetime import datetime
from config import DB_PATH


def init_db():
    with sqlite3.connect(DB_PATH) as db:

        c = db.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS moods(
            user_id integer,
            score integer,
            date text
        )""")

        c.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id integer PRIMARY_KEY,
            name text
        )""")


def register(name: str, user_id: int):

    with sqlite3.connect(DB_PATH) as db:

        c = db.cursor()

        c.execute("INSERT INTO users (name, user_id) VALUES(?, ?)", (name, user_id))


def get_name(user_id: int):

    with sqlite3.connect(DB_PATH) as db:

        c = db.cursor()

        c.execute("SELECT name FROM users WHERE user_id = ? ORDER BY rowid DESC LIMIT 1", (user_id,))

        result = c.fetchone()

        if result:
            return result[0]
        return None


def save_mood(score: int, user_id: int):

    now = datetime.now().strftime("%Y-%m-%d")

    with sqlite3.connect(DB_PATH) as db:

        c = db.cursor()

        c.execute("INSERT INTO moods (user_id, score, date) VALUES(?, ?, ?)",(user_id, score, now))


def get_last_mood(user_id: int):
    with sqlite3.connect(DB_PATH) as db:
    
            c = db.cursor()

            c.execute("SELECT score, date FROM moods WHERE user_id = ? ORDER BY rowid DESC LIMIT 1",(user_id,)) 

            return c.fetchone()


def get_average_mood(user_id: int):
    with sqlite3.connect(DB_PATH) as db:

        c = db.cursor()

        c.execute("SELECT score FROM moods WHERE user_id = ? ORDER BY rowid DESC LIMIT 7" ,(user_id,))

        result = c.fetchall()

        return result


def check_mood_today(user_id: int):
    today = datetime.now().strftime("%Y-%m-%d")
    
    with sqlite3.connect(DB_PATH) as db:
        
        c = db.cursor()

        c.execute("SELECT * FROM moods WHERE user_id = ? AND date = ?",(user_id, today))
        result = c.fetchone()

    return result is not None 
    