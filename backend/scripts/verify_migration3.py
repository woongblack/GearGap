"""마이그레이션 #3 검증 — 스키마 + FK + 행 수"""
import sqlite3

conn = sqlite3.connect("geargap_dev.db")

print("=== 1. 테이블 스키마 ===")
for table in ("contents", "encounters", "drop_sources"):
    print(f"\n-- {table} --")
    rows = conn.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}'").fetchone()
    print(rows[0] if rows else "NOT FOUND")

print("\n=== 2. FK 무결성 — drop_sources ===")
fks = conn.execute("PRAGMA foreign_key_list(drop_sources)").fetchall()
for fk in fks:
    print(f"  id={fk[0]} seq={fk[1]} table={fk[2]} from={fk[3]} to={fk[4]}")

print("\n=== 3. 인덱스/제약 — drop_sources ===")
idxs = conn.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='drop_sources'").fetchall()
for idx in idxs:
    print(f"  {idx[0]}: {idx[1]}")

print("\n=== 4. 행 수 확인 ===")
for table in ("contents", "encounters", "drop_sources", "spec_slot_item_popularity"):
    cnt = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {cnt}행")

conn.close()
