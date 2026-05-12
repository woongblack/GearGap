"""Murlok.io — 슬롯별 아이템 + 픽률 전체 추출"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}
URL = "https://murlok.io/warlock/destruction/m+"

soup = BeautifulSoup(httpx.get(URL, timeout=15, headers=HEADERS, follow_redirects=True).text, "html.parser")

# 1. ol 첫 번째 아이템 내부 구조 상세 파악
print("=== <ol> 내부 구조 상세 (Head 슬롯 첫 번째 아이템) ===")
h3_head = soup.find("h3", string="Head")
parent_div = h3_head.parent
ol = parent_div.find("ol")
if ol:
    first_li = ol.find("li")
    if first_li:
        print(f"li html:\n{first_li.prettify()[:1500]}")

# 2. 전체 슬롯 × 아이템 추출
print("\n\n=== 전체 슬롯 파싱 ===")
section = soup.find("section", class_="wow-equipment-slots")
if not section:
    print("wow-equipment-slots 섹션 없음")
    sys.exit(1)

slot_boxes = section.find_all("div", recursive=False)
print(f"슬롯 수: {len(slot_boxes)}\n")

results = {}
for box in slot_boxes:
    h3 = box.find("h3")
    if not h3:
        continue
    slot_name = h3.text.strip()
    ol = box.find("ol")
    if not ol:
        continue

    items = []
    for li in ol.find_all("li"):
        item_text = li.get_text(separator=" ", strip=True)
        items.append(item_text)

    results[slot_name] = items
    print(f"[{slot_name}] ({len(items)}개 후보)")
    for item in items[:3]:
        print(f"  - {item[:100]}")
    if len(items) > 3:
        print(f"  ... +{len(items)-3}개")
    print()

print(f"\n총 {len(results)}개 슬롯 파싱 완료")
