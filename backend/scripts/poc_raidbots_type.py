"""Raidbots type 필드 및 구조 추가 확인"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from dotenv import load_dotenv

load_dotenv()

hash_val = os.getenv("RAIDBOTS_HASH", "")
url = f"https://www.raidbots.com/static/data/{hash_val}/instances.json"
r = httpx.get(
    url,
    headers={"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"},
    timeout=20,
)
data = r.json()

print("=== type 값 목록 ===")
types: dict = {}
for inst in data:
    t = inst.get("type", "?")
    if t not in types:
        types[t] = []
    types[t].append(inst.get("name", "?"))

for t, names in types.items():
    print(f"  type={t!r}:")
    for n in names:
        print(f"    - {n}")

print()
print("=== instance 샘플 (전체) ===")
for inst in data:
    enc_count = len(inst.get("encounters", []))
    enc_sample = [e.get("id") for e in inst.get("encounters", [])[:2]]
    print(f"  id={inst['id']:>6} | type={str(inst.get('type','?')):<10} | enc={enc_count} | {inst['name']!r}")

print()
print("=== encounter 객체 전체 샘플 (첫 3개) ===")
for inst in data[:3]:
    for enc in inst.get("encounters", [])[:2]:
        print(f"  instance={inst['name']!r} | encounter={enc}")
