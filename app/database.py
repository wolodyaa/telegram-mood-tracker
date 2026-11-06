import sqlite3
from datetime import datetime
from config import DB_PATH


def init_db():
    with sqlite3.connect(DB_PATH) as db:

        c = db.cursor()

        c.execute(""" CREATE TABLE IF NOT EXISTS moods(
            user_id integer,
            score integer,
            date text
        )""")

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

def check_mood_today(user_id: int):
    today = datetime.now().strftime("%Y-%m-%d")
    
    with sqlite3.connect(DB_PATH) as db:
        
        c = db.cursor()

        c.execute("SELECT * FROM moods WHERE user_id = ? AND date = ?",(user_id, today))
        result = c.fetchone()

    return result is not None 
    