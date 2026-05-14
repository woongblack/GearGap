"""ingestion 검증 — 흑마 어둠 BiS 트링켓 드롭처 쿼리"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import text
from app.core.db import engine

# 1. 기본 카운트
with engine.connect() as conn:
    counts = {
        "contents":    conn.execute(text("SELECT COUNT(*) FROM contents")).scalar(),
        "encounters":  conn.execute(text("SELECT COUNT(*) FROM encounters")).scalar(),
        "items":       conn.execute(text("SELECT COUNT(*) FROM items")).scalar(),
        "drop_sources": conn.execute(text("SELECT COUNT(*) FROM drop_sources")).scalar(),
    }
    print("=== 테이블 카운트 ===")
    for k, v in counts.items():
        print(f"  {k:<15}: {v}")

    # 2. 흑마 어둠 BiS 트링켓 드롭처 (끝나는 신호)
    print("\n=== 흑마(파멸) BiS 트링켓 드롭처 ===")
    rows = conn.execute(text("""
        SELECT
            c.name_en   AS instance,
            e.name      AS encounter,
            ssip.item_name,
            ssip.count
        FROM spec_slot_item_popularity ssip
        JOIN drop_sources ds   ON ds.item_id      = ssip.item_id
        JOIN encounters   e    ON ds.encounter_id = e.id
        JOIN contents     c    ON e.content_id    = c.id
        WHERE ssip.class_name  = 'warlock'
          AND ssip.spec_name   = 'destruction'
          AND ssip.slot        = 'trinkets'
        ORDER BY ssip.count DESC
        LIMIT 5
    """)).fetchall()

    if not rows:
        print("  (결과 없음 — BiS 트링켓 item_id가 drop_sources에 없음)")
    for r in rows:
        print(f"  [{r.count}/50]  {r.item_name!r:<40}  {r.instance!r} / {r.encounter!r}")
