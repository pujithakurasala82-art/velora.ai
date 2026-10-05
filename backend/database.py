
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent.parent / "veylora.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        profile_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        assessment_type TEXT NOT NULL,
        score REAL NOT NULL,
        total INTEGER NOT NULL,
        answers_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        career TEXT NOT NULL,
        score REAL NOT NULL,
        explanation TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )""")
    conn.commit()
    conn.close()

def save_student(profile):
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students(name, profile_json, created_at) VALUES (?, ?, ?)",
        (profile.get("name", "Student"), json.dumps(profile), datetime.now(timezone.utc).isoformat())
    )
    student_id = cur.lastrowid
    conn.commit()
    conn.close()
    return student_id

def save_assessment(student_id, assessment_type, score, total, answers):
    init_db()
    conn = get_connection()
    conn.execute(
        """INSERT INTO assessments(student_id, assessment_type, score, total, answers_json, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (student_id, assessment_type, score, total, json.dumps(answers),
         datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()

def save_recommendations(student_id, recommendations):
    init_db()
    conn = get_connection()
    for item in recommendations:
        conn.execute(
            """INSERT INTO recommendations(student_id, career, score, explanation, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (student_id, item.get("career",""), item.get("compatibility_score",0),
             item.get("why_suitable",""), datetime.now(timezone.utc).isoformat())
        )
    conn.commit()
    conn.close()
