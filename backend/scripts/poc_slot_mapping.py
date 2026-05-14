"""main_hand/off_hand BiS item_id → inventoryType 대조"""
import io, os, sys, sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import httpx
from dotenv import load_dotenv
load_dotenv()

hash_val = os.getenv("RAIDBOTS_HASH", "")
conn = sqlite3.connect("geargap_dev.db")

QUERIES = [
    ("warlock", "affliction",    "main_hand"),
    ("warlock", "affliction",    "off_hand"),
    ("warlock", "destruction",   "main_hand"),
    ("warlock", "destruction",   "off_hand"),
    ("hunter",  "marksmanship",  "main_hand"),
    ("hunter",  "beast_mastery", "main_hand"),
]

# DB에서 BiS item_id 수집
target_ids: set[int] = set()
query_results: dict[tuple, list] = {}

for cls, spec, slot in QUERIES:
    rows = conn.execute(
        "SELECT item_name, item_id, count FROM spec_slot_item_popularity "
        "WHERE class_name=? AND spec_name=? AND slot=? ORDER BY count DESC LIMIT 5",
        (cls, spec, slot)
    ).fetchall()
    key = (cls, spec, slot)
    query_results[key] = rows
    for _, item_id, _ in rows:
        target_ids.add(item_id)

conn.close()

print(f"조회 대상 item_id {len(target_ids)}개 수집 완료")

# equippable-items.json에서 해당 item_id의 inventoryType 조회
print("\nFetching equippable-items.json...")
r = httpx.get(
    f"https://www.raidbots.com/static/data/{hash_val}/equippable-items.json",
    headers={"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"},
    timeout=60,
)
items = r.json()

inv_map: dict[int, dict] = {
    it["id"]: it for it in items
    if isinstance(it, dict) and it.get("id") in target_ids
}
print(f"매칭된 아이템: {len(inv_map)}개 / {len(target_ids)}개")

# 결과 출력
INV_NAMES = {
    13: "One-Hand", 14: "Shield", 15: "Ranged(bow)",
    16: "Back", 17: "Two-Hand", 21: "Main Hand",
    22: "Off Hand", 23: "Held In Off-hand",
    26: "Ranged-Right(wand/gun/xbow)",
}

for cls, spec, slot in QUERIES:
    rows = query_results[(cls, spec, slot)]
    if not rows:
        continue
    print(f"\n=== {cls}/{spec} | slot={slot} ===")
    for item_name, item_id, count in rows:
        inv_data = inv_map.get(item_id)
        if inv_data:
            inv_type = inv_data.get("inventoryType", "MISSING")
            label = INV_NAMES.get(inv_type, f"type{inv_type}")
            print(f"  count={count:2d} | {item_name!r:45} id={item_id} | invType={inv_type}({label})")
        else:
            print(f"  count={count:2d} | {item_name!r:45} id={item_id} | → equippable-items에 없음")
