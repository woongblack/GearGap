import sqlite3
conn = sqlite3.connect("geargap_dev.db")
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
for t in tables:
    cols = conn.execute(f"PRAGMA table_info({t[0]})").fetchall()
    col_names = [c[1] for c in cols]
    print(f"{t[0]}: {col_names}")
conn.close()
