import sqlite3
import uuid

def init_db():
    conn = sqlite3.connect('extractions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS extraction (
            id TEXT PRIMARY KEY, 
            extracted_content TEXT, 
            type_of_extraction TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_extraction(content, extraction_type):
    init_db()
    conn = sqlite3.connect('extractions.db')
    c = conn.cursor()
    new_id = str(uuid.uuid4())
    c.execute("INSERT INTO extraction (id, extracted_content, type_of_extraction) VALUES (?, ?, ?)",
              (new_id, content, extraction_type))
    conn.commit()
    conn.close()
    return new_id

def get_all_extractions():
    init_db()
    conn = sqlite3.connect('extractions.db')
    c = conn.cursor()
    c.execute("SELECT id, extracted_content, type_of_extraction FROM extraction")
    data = c.fetchall()
    conn.close()
    return data

def get_extraction_by_id(extraction_id):
    init_db()
    conn = sqlite3.connect('extractions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM extraction WHERE id = ?", (extraction_id,))
    data = c.fetchone()
    conn.close()
    return data

def update_extraction(extraction_id, content):
    conn = sqlite3.connect('extractions.db')
    c = conn.cursor()
    c.execute("UPDATE extraction SET extracted_content = ? WHERE id = ?", (content, extraction_id))
    conn.commit()
    conn.close()

def delete_extraction(extraction_id):
    conn = sqlite3.connect('extractions.db')
    c = conn.cursor()
    c.execute("DELETE FROM extraction WHERE id = ?", (extraction_id,))
    conn.commit()
    conn.close()