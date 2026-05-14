"""inventoryType=-1 아이템 정체 확인"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import httpx
from dotenv import load_dotenv
load_dotenv()

hash_val = os.getenv("RAIDBOTS_HASH", "")
VALID_TYPES = {"dungeon", "raid"}

inst_r = httpx.get(
    f"https://www.raidbots.com/static/data/{hash_val}/instances.json",
    headers={"User-Agent": "GearGap/0.1"}, timeout=20,
)
valid_ids = {
    inst["id"] for inst in inst_r.json()
    if inst["id"] > 0 and inst["type"] in VALID_TYPES
}

item_r = httpx.get(
    f"https://www.raidbots.com/static/data/{hash_val}/equippable-items.json",
    headers={"User-Agent": "GearGap/0.1"}, timeout=60,
)
items = item_r.json()

print("=== inventoryType=-1 전체 목록 (현재 시즌 드롭) ===")
for it in items:
    if not isinstance(it, dict) or it.get("inventoryType", 0) != -1:
        continue
    if not it.get("sources"):
        continue
    for src in it["sources"]:
        if src.get("instanceId", 0) in valid_ids:
            print(f"  id={it['id']} | name={it['name']!r} | quality={it.get('quality')} | itemClass={it.get('itemClass')} | sources={it['sources']}")
            break
