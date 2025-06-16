import sqlite3
import os
from tkinter import messagebox


class Database:
    def __init__(self):
        dbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mini_allegro.db")
        
        if not os.path.exists(dbPath):
            messagebox.showwarning("Uwaga", "Nie odnaleziono bazydanych mini_allegro.db!")

        self.conn = sqlite3.connect(dbPath)

    def get_all(self, sql, params=None):
        cursor = self.conn.cursor()
        
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        return cursor.fetchall()
        
    def get_one(self, sql, params=None):
        cursor = self.conn.cursor()
        
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        return cursor.fetchone()

    def run(self, sql, params=None):
        cursor = self.conn.cursor()
        
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        self.conn.commit()

        return cursor.lastrowid