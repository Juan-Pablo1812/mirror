# db.py - sqlite helpers: log + pending_operations
import sqlite3, threading, os

_lock = threading.Lock()

def init_db(path=None):
    if path is None:
        path = os.path.join(os.getcwd(), "sync.db")
    conn = sqlite3.connect(path, check_same_thread=False)
    with _lock:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS log (
                        id TEXT PRIMARY KEY, action TEXT, path TEXT,
                        timestamp TEXT, status TEXT, note TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS pending (
                        id TEXT PRIMARY KEY, header TEXT, retries INTEGER DEFAULT 0,
                        created_at TEXT
                    )''')
        conn.commit()
    return conn

def insert_log(conn, id, action, path, timestamp, status="pending", note=None):
    with _lock:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO log (id,action,path,timestamp,status,note) VALUES (?,?,?,?,?,?)",
                  (id, action, path, timestamp, status, note))
        conn.commit()

def update_log_status(conn, id, status, note=None):
    with _lock:
        c = conn.cursor()
        c.execute("UPDATE log SET status=?, note=? WHERE id=?", (status, note, id))
        conn.commit()

def add_pending(conn, id, header_bytes):
    with _lock:
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO pending (id, header, retries, created_at) VALUES (?,?,0,datetime('now'))",
                  (id, header_bytes.decode('latin1')))
        conn.commit()

def remove_pending(conn, id):
    with _lock:
        c = conn.cursor()
        c.execute("DELETE FROM pending WHERE id=?", (id,))
        conn.commit()

def list_pending(conn):
    with _lock:
        c = conn.cursor()
        c.execute("SELECT id, header, retries FROM pending")
        rows = c.fetchall()
        return rows

def increment_retry(conn, id):
    with _lock:
        c = conn.cursor()
        c.execute("UPDATE pending SET retries = retries + 1 WHERE id=?", (id,))
        conn.commit()
