"""smoke test JSON에서 DB 스키마 설계용 수치 추출"""
import io, sys, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

data = json.loads(Path("data/murlok_smoke_test_results.json").read_text(encoding="utf-8"))
all_items = [
    it
    for spec in data["specs"]
    for items in spec["slots"].values()
    for it in items
]

# item_id
ids = [it["item_id"] for it in all_items]
print(f"item_id: min={min(ids)}, max={max(ids)}, 총 {len(ids)}개")
print(f"  PostgreSQL int (2^31-1 = {2**31-1}) 범위 내: {max(ids) < 2**31}")

# item_name
names = [it["item_name"] for it in all_items]
lengths = sorted(len(n) for n in names)
print(f"\nitem_name 길이: min={lengths[0]}, max={lengths[-1]}, avg={sum(lengths)/len(lengths):.1f}")
longest = max(names, key=len)
print(f"  가장 긴 이름 ({len(longest)}자): '{longest}'")

# class_name / spec_name
cls_names = sorted(set(s["class_name"] for s in data["specs"]), key=len)
spec_names = sorted(set(s["spec_name"] for s in data["specs"]), key=len)
print(f"\nclass_name: max={len(cls_names[-1])}자 ({cls_names[-1]})")
print(f"spec_name:  max={len(spec_names[-1])}자 ({spec_names[-1]})")

# count 범위
counts = [it["count"] for it in all_items]
print(f"\ncount: min={min(counts)}, max={max(counts)}, total_sample=50 고정")

# 슬롯별 아이템 수
print("\n슬롯당 아이템 수 (전 스펙):")
for slot, stat in sorted(data["slot_stats"].items()):
    mn = stat["min"]
    mx = stat["max"]
    avg = stat["avg"]
    n = stat["spec_count"]
    print(f"  {slot:<14} min={mn}  max={mx}  avg={avg}  (n={n}개 스펙)")

# 전체 행 수 추정
total_rows = len(all_items)
print(f"\n전체 아이템 행 수 (26 스펙): {total_rows}개")
print(f"  -> varchar(100) item_name 충분: {lengths[-1] <= 100}")
