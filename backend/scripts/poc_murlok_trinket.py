"""Murlok 트링켓 조합 데이터 존재 여부 확인"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}

def fetch(url: str) -> BeautifulSoup:
    r = httpx.get(url, timeout=15, headers=HEADERS, follow_redirects=True)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

soup = fetch("https://murlok.io/warlock/destruction/m+")

# 1. "combo", "combination", "pair", "synergy" 키워드 탐색
print("=== 조합 관련 키워드 탐색 ===")
keywords = ["combo", "combination", "pair", "synergy", "together", "with"]
for kw in keywords:
    hits = soup.find_all(string=re.compile(kw, re.I))
    if hits:
        print(f"'{kw}' — {len(hits)}건:")
        for h in hits[:2]:
            print(f"  '{h.strip()[:100]}'")

# 2. section 전체 목록 + h2/h3 헤더
print("\n=== 모든 section 헤더 ===")
for sec in soup.find_all("section"):
    cls = sec.get("class", [])
    h = sec.find(["h2", "h3"])
    header_text = h.text.strip() if h else "(헤더 없음)"
    print(f"  section.{cls}: '{header_text}'")

# 3. Trinkets 슬롯 주변 전체 HTML 출력
print("\n=== Trinkets 슬롯 div 전체 구조 ===")
section = soup.find("section", class_="wow-equipment-slots")
for box in section.find_all("div", recursive=False):
    h3 = box.find("h3")
    if h3 and h3.text.strip() == "Trinkets":
        print(box.prettify()[:3000])
        break

# 4. 트링켓 전용 별도 섹션 존재 여부
print("\n=== 트링켓 전용 섹션 탐색 ===")
trinket_sections = soup.find_all(
    lambda tag: tag.name in ["section", "div"] and
    any("trinket" in c.lower() for c in tag.get("class", []))
)
print(f"'trinket' class 포함 요소: {len(trinket_sections)}개")
for t in trinket_sections[:3]:
    print(f"  <{t.name}> class={t.get('class')} | text앞50: {t.get_text(strip=True)[:50]}")
