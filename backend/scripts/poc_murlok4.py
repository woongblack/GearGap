"""Murlok.io — 정식 파서 (아이템ID + 이름 + 픽률 + 태그)"""
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}
URL = "https://murlok.io/warlock/destruction/m+"

soup = BeautifulSoup(httpx.get(URL, timeout=15, headers=HEADERS, follow_redirects=True).text, "html.parser")

# 샘플 크기 탐색
sample_size = None
for el in soup.find_all(string=re.compile(r'\d+\s*/\s*\d+|\d+\s+characters?|\d+\s+players?', re.I)):
    print(f"[샘플 크기 후보] '{el.strip()}'")
    m = re.search(r'(\d+)', el.strip())
    if m:
        sample_size = int(m.group(1))

# 상단 메타 정보 탐색
print("\n[메타 정보]")
for el in soup.find_all(["p", "span", "small"], class_=re.compile(r'info|meta|sample|count|stat', re.I)):
    t = el.get_text(strip=True)
    if t:
        print(f"  {el.name}.{el.get('class')}: {t[:100]}")

# 전체 섹션에서 숫자가 있는 작은 텍스트 탐색
print("\n[숫자 포함 텍스트 (상위 20개)]")
for el in soup.find_all(string=re.compile(r'^\d+$')):
    parent = el.parent
    gp = parent.parent if parent else None
    context = gp.get_text(separator=" ", strip=True)[:60] if gp else ""
    print(f"  '{el.strip()}' ← <{parent.name}> | context: {context}")


print("\n\n=== 슬롯별 아이템 정식 파싱 ===\n")

section = soup.find("section", class_="wow-equipment-slots")
slot_boxes = section.find_all("div", recursive=False)

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
    # vi-poppable li만 (중첩 li 제외)
    for li in ol.find_all("li", class_="vi-poppable", recursive=False):
        # Wowhead 링크 → 아이템 ID
        a = li.find("a", href=re.compile(r'wowhead\.com/item='))
        if not a:
            continue
        href = a.get("href", "")
        item_id_match = re.search(r'/item=(\d+)', href)
        item_id = int(item_id_match.group(1)) if item_id_match else None

        # 아이템 이름
        h4 = li.find("h4")
        item_name = h4.text.strip() if h4 else "?"

        # ul > li 리스트: 태그(Set/Craft) + 카운트
        ul = li.find("ul")
        tag_type = None
        count = None
        if ul:
            lis = ul.find_all("li", recursive=False)
            if len(lis) >= 1:
                tag_text = lis[0].get_text(strip=True)
                if tag_text in ("Set", "Craft", "Legendary"):
                    tag_type = tag_text
            if len(lis) >= 2:
                count_text = lis[-1].get_text(strip=True)
                m = re.search(r'(\d+)', count_text)
                if m:
                    count = int(m.group(1))

        items.append({
            "item_id": item_id,
            "name": item_name,
            "tag": tag_type,
            "count": count,
            "wowhead_url": href,
        })

    results[slot_name] = items
    print(f"[{slot_name}]")
    for it in items:
        cnt = it["count"] or 0
        bar = "█" * cnt + "░" * max(0, 20 - cnt)
        tag = f" [{it['tag']}]" if it["tag"] else ""
        print(f"  {bar} {cnt:>3}/??  {it['name']}{tag}  (ID: {it['item_id']})")
    print()

print(f"총 {len(results)}개 슬롯")
print("\n[JSON 출력 샘플 (Head)]")
print(json.dumps(results.get("Head", []), ensure_ascii=False, indent=2))
