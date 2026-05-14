"""equippable-items.json에서 distinct inventoryType 수집
현재 시즌 드롭 아이템 기준 + 전체 아이템 기준 비교"""
import io
import os
import sys
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from dotenv import load_dotenv

load_dotenv()

hash_val = os.getenv("RAIDBOTS_HASH", "")

# instances.json로 현재 시즌 valid_ids 구성
VALID_TYPES = {"dungeon", "raid"}
inst_r = httpx.get(
    f"https://www.raidbots.com/static/data/{hash_val}/instances.json",
    headers={"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"},
    timeout=20,
)
valid_ids = {
    inst["id"]
    for inst in inst_r.json()
    if inst["id"] > 0 and inst["type"] in VALID_TYPES
}
print(f"현재 시즌 valid instance IDs: {len(valid_ids)}개 — {sorted(valid_ids)}")

# equippable-items.json fetch
print("\nFetching equippable-items.json (52MB)...")
item_r = httpx.get(
    f"https://www.raidbots.com/static/data/{hash_val}/equippable-items.json",
    headers={"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"},
    timeout=60,
)
items = item_r.json()
print(f"전체 아이템: {len(items):,}개")

# 현재 시즌 드롭 아이템 분리
current_season: list = []
for it in items:
    if not isinstance(it, dict) or not it.get("sources"):
        continue
    for src in it["sources"]:
        if src.get("instanceId", 0) in valid_ids:
            current_season.append(it)
            break

print(f"현재 시즌 드롭 아이템: {len(current_season)}개")

# inventoryType 분석 — 현재 시즌 기준
print("\n=== 현재 시즌 드롭 아이템 inventoryType 분포 ===")
inv_stats: dict[int, dict] = defaultdict(lambda: {"count": 0, "examples": []})

for it in current_season:
    inv = it.get("inventoryType", -1)
    inv_stats[inv]["count"] += 1
    if len(inv_stats[inv]["examples"]) < 2:
        inv_stats[inv]["examples"].append(it.get("name", "?"))

# WoW inventoryType 공식 명칭 참조
INV_NAMES = {
    0: "None/Non-Equip",
    1: "Head",
    2: "Neck",
    3: "Shoulder",
    4: "Shirt",
    5: "Chest",
    6: "Waist",
    7: "Legs",
    8: "Feet",
    9: "Wrist",
    10: "Hands",
    11: "Finger",
    12: "Trinket",
    13: "One-Hand",
    14: "Shield",
    15: "Ranged (Hunter bow)",
    16: "Back (Cloak)",
    17: "Two-Hand",
    18: "Bag",
    19: "Tabard",
    20: "Chest (Robe)",
    21: "Main Hand",
    22: "Off Hand (item)",
    23: "Held In Off-hand",
    24: "Ammo",
    25: "Thrown",
    26: "Ranged-Right (wand/gun/xbow)",
    28: "Relic",
}

for inv_type in sorted(inv_stats.keys()):
    stat = inv_stats[inv_type]
    label = INV_NAMES.get(inv_type, f"Unknown({inv_type})")
    examples = ", ".join(stat["examples"])
    print(f"  [{inv_type:2d}] {label:<30} count={stat['count']:3d}  ex: {examples}")

# quality 분포도
print("\n=== 현재 시즌 quality 분포 ===")
qual_stats: dict[int, int] = defaultdict(int)
QUAL_NAMES = {1: "Common", 2: "Uncommon", 3: "Rare(Blue)", 4: "Epic(Purple)", 5: "Legendary"}
for it in current_season:
    qual_stats[it.get("quality", -1)] += 1
for q in sorted(qual_stats.keys()):
    print(f"  [{q}] {QUAL_NAMES.get(q, '?'):<15} count={qual_stats[q]}")
