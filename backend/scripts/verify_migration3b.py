import io, sys, sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

conn = sqlite3.connect("geargap_dev.db")

print("=== FK: drop_sources ===")
for fk in conn.execute("PRAGMA foreign_key_list(drop_sources)").fetchall():
    print(f"  from={fk[3]} -> {fk[2]}.{fk[4]}")

print("\n=== row counts ===")
for t in ("contents", "encounters", "drop_sources", "spec_slot_item_popularity"):
    cnt = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t}: {cnt}")

conn.close()
