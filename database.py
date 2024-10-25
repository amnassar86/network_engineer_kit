# database.py

import sqlite3
import os

DB_NAME = 'circuits.db'

def initialize_database():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE circuits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                number TEXT NOT NULL,
                location TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)
