"""스키마 확인 4개 항목"""
import sqlite3

conn = sqlite3.connect("geargap_dev.db")

tables = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
).fetchall()]
print(f"전체 테이블: {tables}")

try:
    rows = conn.execute("SELECT COUNT(*) FROM contents").fetchone()[0]
    print(f"\ncontents 행 수: {rows}")
    if rows > 0:
        for r in conn.execute("SELECT * FROM contents LIMIT 5").fetchall():
            print(f"  {r}")
except Exception as e:
    print(f"contents 오류: {e}")

try:
    rows2 = conn.execute("SELECT COUNT(*) FROM drop_sources").fetchone()[0]
    print(f"\ndrop_sources 행 수: {rows2}")
except Exception as e:
    print(f"drop_sources 오류: {e}")

print("\ncontents 컬럼:")
for col in conn.execute("PRAGMA table_info(contents)").fetchall():
    print(f"  {col}")

print("\ndrop_sources 컬럼:")
for col in conn.execute("PRAGMA table_info(drop_sources)").fetchall():
    print(f"  {col}")

conn.close()
