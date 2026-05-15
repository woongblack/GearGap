import sqlite3

conn = sqlite3.connect("geargap_dev.db")
conn.execute("UPDATE alembic_version SET version_num = ?", ("50a67e541212",))
conn.commit()
print("reset to:", conn.execute("SELECT version_num FROM alembic_version").fetchone()[0])
