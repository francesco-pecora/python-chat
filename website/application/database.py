import sqlite3
from sqlite3 import Error
from datetime import datetime
import time


FILE = "messages.db"
PLAYLIST_TABLE = "Messages"

class DataBase:
    def __init__(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(FILE)
        except Error as e:
            print(e)
        
        self.cursor = self.conn.cursor()
        self._create_table()


    def close(self):
        self.conn.close()


    def _create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {PLAYLIST_TABLE}
                    (name TEXT, content TEXT, time Date, id INTEGER PRIMARY KEY AUTOINCREMENT)"""

        self.cursor.execute(query)
        self.conn.commit()

    
    def get_all_messages(self, limit=100):
        query = f"SELECT * FROM {PLAYLIST_TABLE}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        results = []
        for item in sorted(result, key=lambda x: x[3], reverse=True)[:limit]:
            name, content, date, _id = item
            data = {"name": name, "message":content, "time": str(date)}
            results.append(data)
        
        return list(reversed(results))

    
    def save_message(self, name, msg):
        query = f"INSERT INTO {PLAYLIST_TABLE} VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, msg, datetime.now(), None))
        self.conn.commit()


