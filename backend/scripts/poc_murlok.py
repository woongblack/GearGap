"""
Murlok.io HTML 파싱 PoC
- URL 패턴: https://murlok.io/{class}/{spec}/m+
- 목표: 슬롯별 아이템 + 픽률 추출
"""
import io, sys, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}
URL = "https://murlok.io/warlock/destruction/m+"


def fetch(url: str) -> BeautifulSoup:
    r = httpx.get(url, timeout=15, headers=HEADERS, follow_redirects=True)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def main() -> None:
    print(f"=== Murlok.io 파싱 PoC ===")
    print(f"URL: {URL}\n")

    soup = fetch(URL)

    # 1. 페이지 기본 정보
    title = soup.find("title")
    print(f"[페이지 타이틀] {title.text.strip() if title else '없음'}\n")

    # 2. HTML 구조 탐색 — 슬롯 관련 섹션 찾기
    print("[구조 탐색] 주요 태그 분포:")
    for tag in ["table", "section", "article", "div"]:
        count = len(soup.find_all(tag))
        print(f"  <{tag}>: {count}개")

    # 3. 'uses' 텍스트 주변 구조 확인
    print("\n['uses' 키워드 주변 구조 샘플 (첫 3개)]:")
    uses_elements = soup.find_all(string=re.compile(r'\d+\s*uses?', re.I))
    for i, el in enumerate(uses_elements[:3]):
        parent = el.parent
        grandparent = parent.parent if parent else None
        print(f"  {i+1}. 텍스트: '{el.strip()}'")
        print(f"     부모: <{parent.name}> class={parent.get('class', [])}")
        if grandparent:
            print(f"     조부모: <{grandparent.name}> class={grandparent.get('class', [])}")
        print()

    # 4. 슬롯 헤더 찾기 (Head, Neck, Shoulder 등)
    slot_keywords = ["Head", "Neck", "Shoulder", "Back", "Chest", "Wrist",
                     "Hands", "Waist", "Legs", "Feet", "Finger", "Trinket",
                     "Main Hand", "Off Hand"]
    print("[슬롯 키워드 위치 탐색]:")
    found_slots = []
    for kw in slot_keywords:
        els = soup.find_all(string=re.compile(rf'^{kw}$', re.I))
        if els:
            el = els[0]
            parent = el.parent
            print(f"  '{kw}' → <{parent.name}> class={parent.get('class', [])}")
            found_slots.append(kw)
    print(f"  발견된 슬롯: {len(found_slots)}개\n")

    # 5. JSON-like 데이터 탐색 (script 태그 안에 있을 수도)
    scripts = soup.find_all("script")
    print(f"[Script 태그] 총 {len(scripts)}개")
    for i, s in enumerate(scripts):
        text = s.string or ""
        if any(kw in text for kw in ["item_id", "itemId", "slot", "uses", "popularity", "trinket"]):
            print(f"  script[{i}] — 관련 키워드 발견! 앞 300자:")
            print(f"  {text[:300]}")
            print()

    # 6. 테이블 구조 확인
    tables = soup.find_all("table")
    print(f"\n[테이블] 총 {len(tables)}개")
    for i, t in enumerate(tables[:3]):
        headers = [th.text.strip() for th in t.find_all("th")]
        rows = t.find_all("tr")
        print(f"  table[{i}]: {len(rows)}행 | 헤더: {headers[:6]}")


if __name__ == "__main__":
    main()
