"""Raidbots equippable-items.json PoC — 드롭소스 필드 확인"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from dotenv import load_dotenv

load_dotenv()

hash_val = os.getenv("RAIDBOTS_HASH", "")
url = f"https://www.raidbots.com/static/data/{hash_val}/equippable-items.json"
print(f"Fetching equippable-items.json...")

r = httpx.get(
    url,
    headers={"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"},
    timeout=30,
)
print(f"Status: {r.status_code}, Size: {len(r.content):,} bytes")
if r.status_code != 200:
    print(r.text[:300])
    sys.exit(1)

data = r.json()

# 최상위 구조
if isinstance(data, list):
    items = data
elif isinstance(data, dict) and "items" in data:
    items = data["items"]
else:
    items = list(data.values()) if isinstance(data, dict) else []

print(f"총 아이템 수: {len(items)}")

if not items:
    print("아이템 없음")
    sys.exit(1)

first = items[0]
print(f"\n=== 아이템 객체 키 (첫 번째) ===")
print(f"keys: {list(first.keys()) if isinstance(first, dict) else type(first)}")

# 드롭소스 관련 필드 탐색
DROP_KEYS = [
    "source", "dropSource", "drop_source", "sourceId",
    "instanceId", "instance_id", "encounterId", "encounter_id",
    "journalEncounterId", "journal_encounter_id",
    "sourceType", "source_type",
]

print(f"\n=== 드롭소스 관련 필드 탐색 (전체 {len(items)}개 아이템) ===")
found_keys: dict[str, list] = {}

for item in items:
    if not isinstance(item, dict):
        continue
    for k in item:
        if any(dk.lower() in k.lower() for dk in ["source", "instance", "encounter", "drop", "journal"]):
            if k not in found_keys:
                found_keys[k] = []
            if len(found_keys[k]) < 3:
                found_keys[k].append(item[k])

if found_keys:
    print("  발견된 필드:")
    for k, samples in found_keys.items():
        print(f"  '{k}': {samples}")
else:
    print("  드롭소스 관련 필드 없음")

# bonus ID 구조 확인
print(f"\n=== bonus ID 구조 확인 (첫 번째 아이템) ===")
for k in ["bonusIds", "bonus_ids", "bonuses", "itemBonusIds"]:
    if k in first:
        print(f"  '{k}': {first[k][:5] if isinstance(first[k], list) else first[k]!r}")

print(f"\n=== 첫 번째 아이템 전체 ===")
print(first)

# 아이템 5개 샘플 (키 목록 비교)
print(f"\n=== 아이템 5개 키 비교 ===")
key_sets = set()
for item in items[:20]:
    if isinstance(item, dict):
        key_sets.add(tuple(sorted(item.keys())))
for ks in key_sets:
    print(f"  {list(ks)}")
