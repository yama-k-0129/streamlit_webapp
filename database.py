import sqlite3
import streamlit as st

# Create or connect to the database
conn = sqlite3.connect('work_reports.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS work_reports (
        key TEXT PRIMARY KEY,
        name TEXT,
        date TEXT,
        work TEXT,
        time TEXT,
        switch TEXT
    )
''')
conn.commit()

def insert_profile(daytime, name, date, work, time, switch):
    """Returns the report on successful creation, otherwise raises an error"""
    try:
        with sqlite3.connect('work_reports.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO work_reports (key, name, date, work, time, switch) VALUES (?, ?, ?, ?, ?, ?)",
                      (daytime, name, date, work, time, switch))
            conn.commit()
        return "Profile inserted successfully"
    except Exception as e:
        st.error(f"Error inserting profile: {str(e)}")

def fetch_all_profile():
    """Returns a list of all profiles"""
    try:
        with sqlite3.connect('work_reports.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM work_reports")
            rows = c.fetchall()
        columns = [desc[0] for desc in c.description]
        results = [dict(zip(columns, row)) for row in rows]
        return results
    except Exception as e:
        st.error(f"Error fetching profiles: {str(e)}")

def get_private(daytime):
    """Returns the profile for the given daytime"""
    try:
        with sqlite3.connect('work_reports.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM work_reports WHERE key=?", (daytime,))
            row = c.fetchone()
        return row
    except Exception as e:
        st.error(f"Error fetching profile: {str(e)}")
