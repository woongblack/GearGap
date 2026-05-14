"""instances.json 전체 목록 + 패치 정보 확인"""
import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()
h = os.getenv("RAIDBOTS_HASH", "")
if not h:
    print("ERROR: RAIDBOTS_HASH not set")
    sys.exit(1)

r = httpx.get(
    f"https://www.raidbots.com/static/data/{h}/instances.json",
    headers={"User-Agent": "GearGap/0.1"},
    timeout=20,
)
data = r.json()
print(f"총 {len(data)}개 인스턴스\n")
for inst in data:
    enc_count = len(inst.get("encounters", []))
    print(f"id={inst['id']:5}  type={inst['type']:<12}  enc={enc_count}  {inst['name']!r}")
