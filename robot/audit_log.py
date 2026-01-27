import sqlite3
import datetime
import os

# Database Path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'audit.db')

def init_audit_log():
    """Initialize the audit log database table."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                state TEXT,
                details TEXT,
                status TEXT
            )
            """)
            conn.commit()
            print(f"✅ Audit Log Initialized: {DB_PATH}")
    except Exception as e:
        print(f"❌ Failed to init audit log: {e}")

def log_event(event_type, state, details, status="INFO"):
    """
    Log a system event to the audit database.
    
    Args:
        event_type (str): Category (VERIFY, DISPENSE, SYSTEM, ERROR)
        state (str): Current Robot State
        details (str): JSON or text details
        status (str): SUCCESS, FAILED, INFO
    """
    try:
        timestamp = datetime.datetime.now().isoformat()
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
            INSERT INTO audit (timestamp, event_type, state, details, status)
            VALUES (?, ?, ?, ?, ?)
            """, (timestamp, event_type, str(state), str(details), status))
            conn.commit()
    except Exception as e:
        print(f"⚠️ Audit Log Error: {e}")

# Initialize on module load
init_audit_log()
