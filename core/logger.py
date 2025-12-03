import sqlite3
import json
import os
from datetime import datetime


LOG_DIR = os.path.join(os.getcwd(), 'logs')
DB_PATH = os.path.join(LOG_DIR, 'honeypot.db')
RAW_LOG = os.path.join(LOG_DIR, 'raw.log')


os.makedirs(LOG_DIR, exist_ok=True)


_conn = None


def _connect():
global _conn
if _conn is None:
_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
_conn.execute('''
CREATE TABLE IF NOT EXISTS events (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ts TEXT,
src_ip TEXT,
src_port INTEGER,
service TEXT,
event_type TEXT,
data TEXT
)
''')
_conn.commit()
return _conn
def log_event(src_ip, src_port, service, event_type, data):
conn = _connect()
ts = datetime.utcnow().isoformat() + 'Z'
payload = json.dumps(data, ensure_ascii=False)
conn.execute('INSERT INTO events (ts, src_ip, src_port, service, event_type, data) VALUES (?, ?, ?, ?, ?, ?)',
(ts, src_ip, src_port, service, event_type, payload))
conn.commit()


# also append raw log for quick reading
with open(RAW_LOG, 'a', encoding='utf-8') as f:
f.write(f"{ts} {src_ip}:{src_port} {service} {event_type} {payload}\n")


def query_recent(limit=50):
conn = _connect()
cur = conn.execute('SELECT ts, src_ip, src_port, service, event_type, data FROM events ORDER BY id DESC LIMIT ?', (limit,))
rows = cur.fetchall()
return rows


