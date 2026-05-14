"""equippable-items.json sources 필드 심층 분석"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from dotenv import load_dotenv

load_dotenv()

hash_val = os.getenv("RAIDBOTS_HASH", "")

# instances.json 로드 (instanceId 검증용)
inst_url = f"https://www.raidbots.com/static/data/{hash_val}/instances.json"
inst_r = httpx.get(inst_url, headers={"User-Agent": "GearGap/0.1"}, timeout=20)
instances = {inst["id"]: inst for inst in inst_r.json()}
current_instance_ids = {iid for iid, inst in instances.items() if iid > 0}
print(f"instances.json 양수 ID 개수: {len(current_instance_ids)}")

# equippable-items.json 로드
item_url = f"https://www.raidbots.com/static/data/{hash_val}/equippable-items.json"
item_r = httpx.get(item_url, headers={"User-Agent": "GearGap/0.1"}, timeout=30)
items = item_r.json()
print(f"전체 아이템: {len(items):,}")

# sources 있는 아이템만
with_sources = [it for it in items if isinstance(it, dict) and it.get("sources")]
print(f"sources 있는 아이템: {len(with_sources):,}")

# sources가 있고 현재 시즌 인스턴스에서 드롭되는 아이템
current_season_items = []
for it in with_sources:
    for src in it["sources"]:
        if src.get("instanceId", 0) in current_instance_ids:
            current_season_items.append(it)
            break

print(f"현재 시즌 인스턴스에서 드롭되는 아이템: {len(current_season_items):,}")

# sources 구조 샘플
print(f"\n=== sources 구조 샘플 (5개) ===")
for it in with_sources[:5]:
    print(f"  id={it['id']} | name={it['name']!r} | sources={it['sources']}")

# instanceId와 instances.json 연결 검증
print(f"\n=== instanceId -> instances.json 매핑 검증 ===")
for it in current_season_items[:5]:
    for src in it["sources"]:
        iid = src.get("instanceId")
        if iid and iid > 0 and iid in instances:
            inst_name = instances[iid]["name"]
            enc_id = src.get("encounterId")
            # encounter 찾기
            enc_name = "?"
            for enc in instances[iid].get("encounters", []):
                if enc["id"] == enc_id:
                    enc_name = enc["name"]
                    break
            print(f"  item={it['name']!r} | instance={inst_name!r}(id={iid}) | encounter={enc_name!r}(id={enc_id})")

# encounterId가 encounter.id와 일치하는지 통계
print(f"\n=== encounterId 매핑 커버리지 ===")
matched = 0
unmatched = 0
unmatched_samples = []

for it in current_season_items:
    for src in it["sources"]:
        iid = src.get("instanceId", 0)
        eid = src.get("encounterId")
        if iid <= 0 or iid not in instances:
            continue
        enc_ids = {e["id"] for e in instances[iid].get("encounters", [])}
        if eid in enc_ids:
            matched += 1
        else:
            unmatched += 1
            if len(unmatched_samples) < 3:
                unmatched_samples.append((it["name"], iid, eid))

print(f"  encounterId 매핑 성공: {matched}")
print(f"  encounterId 매핑 실패: {unmatched}")
if unmatched_samples:
    print(f"  실패 샘플: {unmatched_samples}")

# 현재 시즌 인스턴스 커버리지
print(f"\n=== 현재 시즌 인스턴스별 드롭 아이템 수 ===")
inst_item_count: dict = {}
for it in current_season_items:
    for src in it["sources"]:
        iid = src.get("instanceId", 0)
        if iid > 0 and iid in instances:
            inst_item_count[iid] = inst_item_count.get(iid, 0) + 1

for iid, cnt in sorted(inst_item_count.items(), key=lambda x: -x[1]):
    inst_name = instances[iid]["name"]
    inst_type = instances[iid]["type"]
    print(f"  {inst_name!r:35} type={inst_type:<10} items={cnt}")
