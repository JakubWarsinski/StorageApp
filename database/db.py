import sys
sys.dont_write_bytecode = True

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mini_allegro.db")

def get_all_elements(sql, params=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql, params or [])
    elements = cursor.fetchall()
    conn.close()
    return elements

def get_single_element(sql, params=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql, params or [])
    row = cursor.fetchone()
    element = row[0] if row else None
    conn.close()
    return element

def insert_element(sql, params):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    conn.close()