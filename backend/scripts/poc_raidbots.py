"""Raidbots instances.json PoC — 7개 항목 확인"""
import json
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

hash_val = os.getenv("RAIDBOTS_HASH", "")
if not hash_val:
    print("ERROR: RAIDBOTS_HASH not set")
    sys.exit(1)

url = f"https://www.raidbots.com/static/data/{hash_val}/instances.json"
print(f"Fetching instances.json (hash masked)...")

r = httpx.get(
    url,
    headers={"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"},
    timeout=20,
)
print(f"Status: {r.status_code}")
if r.status_code != 200:
    print(r.text[:500])
    sys.exit(1)

data = r.json()

# 최상위 구조 파악
print(f"\n=== 최상위 구조 ===")
if isinstance(data, list):
    print(f"타입: list, 길이: {len(data)}")
    first = data[0] if data else {}
elif isinstance(data, dict):
    print(f"타입: dict, 키: {list(data.keys())}")
    # instances 키가 있으면 그걸 사용
    if "instances" in data:
        data = data["instances"]
        print(f"  -> data['instances'] 사용, 길이: {len(data)}")
        first = data[0] if data else {}
    else:
        first = data
else:
    print(f"타입: {type(data)}")
    sys.exit(1)

# instance 객체 키 확인
print(f"\n=== instance 객체 키 ===")
print(f"keys: {list(first.keys())}")

# 1. instance.id
print(f"\n[결정3-1] instance.id → raidbots_id로 쓸 값인가?")
print(f"  id: {first.get('id', 'MISSING')}")
print(f"  id 타입: {type(first.get('id')).__name__}")

# 2. 영문 이름 키
print(f"\n[결정3-2] 영문 이름 키: name vs name_en?")
for key in ["name", "name_en", "nameEn", "englishName"]:
    if key in first:
        print(f"  '{key}' 존재: {first[key]!r}")
    else:
        print(f"  '{key}' 없음")

# 3. encounters[] 있나?
print(f"\n[결정1-1] encounters[] 있나?")
encounters_key = None
for key in ["encounters", "bosses", "encounter"]:
    if key in first:
        encounters_key = key
        enc_list = first[key]
        print(f"  '{key}' 존재: {len(enc_list)}개")
        break
if not encounters_key:
    print(f"  encounters 관련 키 없음. 전체 키: {list(first.keys())}")

# 4. encounter 객체 분석
if encounters_key and first[encounters_key]:
    enc = first[encounters_key][0]
    print(f"\n[결정1-2] encounter 객체 키: {list(enc.keys())}")

    # encounter 고유 ID
    print(f"\n[결정3-3] encounter에 고유 ID 있나?")
    for key in ["id", "encounterId", "encounter_id"]:
        if key in enc:
            print(f"  '{key}': {enc[key]}")

    # drops/loot/items
    print(f"\n[결정1-2] encounter에 drops/loot/items[] 있나?")
    drop_key = None
    for key in ["items", "loot", "drops", "rewards"]:
        if key in enc:
            drop_key = key
            items = enc[key]
            print(f"  '{key}' 존재: {len(items)}개")
            if items:
                print(f"  첫 번째 아이템 키: {list(items[0].keys()) if isinstance(items[0], dict) else items[0]}")
            break
    if not drop_key:
        print(f"  드롭 관련 키 없음. encounter 전체 키: {list(enc.keys())}")

    # item_id 형태
    if drop_key and first[encounters_key][0][drop_key]:
        item0 = first[encounters_key][0][drop_key][0]
        print(f"\n[결정1-3] item_id 형태인가?")
        if isinstance(item0, dict):
            for key in ["id", "item_id", "itemId"]:
                if key in item0:
                    print(f"  '{key}': {item0[key]} (타입: {type(item0[key]).__name__})")
        else:
            print(f"  아이템이 dict가 아님: {type(item0).__name__} = {item0!r}")

# 5. 던전/레이드 구조 동일한가?
print(f"\n[결정1-4] 던전/레이드 구조 동일한가?")
raid_ex = None
dungeon_ex = None
for inst in data:
    kind = inst.get("type", inst.get("kind", inst.get("category", "?")))
    if "raid" in str(kind).lower() and not raid_ex:
        raid_ex = inst
    if ("dungeon" in str(kind).lower() or "mythic" in str(kind).lower()) and not dungeon_ex:
        dungeon_ex = inst

if raid_ex:
    print(f"  레이드 예시: {raid_ex.get('name', '?')} | keys: {list(raid_ex.keys())}")
if dungeon_ex:
    print(f"  던전 예시: {dungeon_ex.get('name', '?')} | keys: {list(dungeon_ex.keys())}")
if not raid_ex or not dungeon_ex:
    # type 키 값 목록 출력
    types = set(inst.get("type", inst.get("kind", "?")) for inst in data)
    print(f"  type/kind 값 목록: {types}")
    print(f"  전체 instance 목록:")
    for inst in data[:10]:
        print(f"    {inst.get('id', '?')} | {inst.get('name', '?')} | type={inst.get('type', inst.get('kind', '?'))}")

print(f"\n=== 완료 ===")
