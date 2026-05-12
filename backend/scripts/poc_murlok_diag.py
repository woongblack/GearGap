"""
Murlok 파싱 진단 스크립트
우선순위 1: 분모(total_sample) 위치 탐색
우선순위 2: count=None 케이스 구조 출력
"""
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}

SPECS = [
    ("warlock", "destruction"),   # 비메타
    ("death-knight", "unholy"),   # 메타 강자 (비교용)
    ("warrior", "arms"),          # 추가 비교
]


def fetch_soup(cls: str, spec: str) -> BeautifulSoup:
    url = f"https://murlok.io/{cls}/{spec}/m+"
    r = httpx.get(url, timeout=15, headers=HEADERS, follow_redirects=True)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser"), url


def find_total_sample(soup: BeautifulSoup) -> tuple[int | None, str]:
    """분모(total_sample) 찾기 — 위치와 값 반환"""

    # 후보 1: "N players", "N characters", "N/50" 패턴
    for pattern in [
        r'(\d+)\s+players?',
        r'(\d+)\s+characters?',
        r'sample[^0-9]*(\d+)',
        r'(\d+)\s*/\s*\d+',
        r'top\s+(\d+)',
        r'based on\s+(\d+)',
    ]:
        for el in soup.find_all(string=re.compile(pattern, re.I)):
            m = re.search(pattern, el.strip(), re.I)
            if m:
                return int(m.group(1)), f"'{el.strip()[:80]}'"

    # 후보 2: 랭킹 테이블 마지막 rank 번호 (순위 목록에서 최대값)
    rank_nums = []
    for el in soup.find_all(string=re.compile(r'^\d+$')):
        parent = el.parent
        context = (parent.parent.get_text(separator=" ", strip=True) if parent.parent else "")
        # 랭킹 컨텍스트: 이름 + 서버 + 점수가 함께 있음
        if re.search(r'\d{3,4}$', context):  # 점수(M+ 점수)가 있는 행
            try:
                rank_nums.append(int(el.strip()))
            except ValueError:
                pass

    # 후보 3: 플레이어 목록의 항목 수 직접 세기
    player_section = soup.find("section", class_=re.compile(r'player|ranking|character|leaderboard', re.I))
    if player_section:
        player_items = player_section.find_all("li")
        if player_items:
            return len(player_items), f"<section class=player*> li 수"

    # 후보 4: 페이지 내 최대 rank 번호
    if rank_nums:
        return max(rank_nums), f"rank 목록 최대값 (후보)"

    return None, "못 찾음"


def inspect_slot_items(soup: BeautifulSoup) -> dict:
    """슬롯별 아이템 파싱 + None 케이스 구조 출력"""
    section = soup.find("section", class_="wow-equipment-slots")
    if not section:
        return {}

    results = {}
    none_cases = []

    for box in section.find_all("div", recursive=False):
        h3 = box.find("h3")
        if not h3:
            continue
        slot_name = h3.text.strip()
        ol = box.find("ol")
        if not ol:
            continue

        items = []
        for li in ol.find_all("li", class_="vi-poppable", recursive=False):
            a = li.find("a", href=re.compile(r'wowhead\.com/item='))
            if not a:
                continue
            href = a.get("href", "")
            item_id_m = re.search(r'/item=(\d+)', href)
            item_id = int(item_id_m.group(1)) if item_id_m else None

            h4 = li.find("h4")
            item_name = h4.text.strip() if h4 else "?"

            # count 추출 — 다양한 패턴 시도
            count = None
            ul = li.find("ul")
            if ul:
                lis = ul.find_all("li", recursive=False)
                # 마지막 li에서 숫자 추출
                for candidate_li in reversed(lis):
                    text = candidate_li.get_text(strip=True)
                    m = re.search(r'^(\d+)$', text)
                    if m:
                        count = int(m.group(1))
                        break
                    # SVG 제거 후 숫자만
                    for svg in candidate_li.find_all("svg"):
                        svg.decompose()
                    clean = candidate_li.get_text(strip=True)
                    m = re.search(r'^(\d+)$', clean)
                    if m:
                        count = int(m.group(1))
                        break

            if count is None:
                none_cases.append({
                    "slot": slot_name,
                    "item": item_name,
                    "ul_html": str(ul)[:400] if ul else "None",
                })

            items.append({"item_id": item_id, "name": item_name, "count": count})

        results[slot_name] = items

    return results, none_cases


def main():
    for cls, spec in SPECS:
        print(f"\n{'='*60}")
        print(f"[{cls}/{spec}]")
        print('='*60)

        soup, url = fetch_soup(cls, spec)

        # 우선순위 1: 분모 찾기
        total, source = find_total_sample(soup)
        print(f"total_sample: {total} (출처: {source})")

        # 우선순위 2: 슬롯 파싱 + None 케이스
        results, none_cases = inspect_slot_items(soup)
        slot_count = len(results)
        item_count = sum(len(v) for v in results.values())
        none_count = len(none_cases)
        print(f"슬롯: {slot_count}개 | 아이템: {item_count}개 | count=None: {none_count}개")

        # 슬롯별 요약
        for slot, items in results.items():
            counts = [i["count"] for i in items]
            none_slots = [i["name"] for i in items if i["count"] is None]
            print(f"  {slot:<12} {len(items)}개  counts={counts[:5]}{'...' if len(counts)>5 else ''}  none={none_slots}")

        # None 케이스 구조 상세
        if none_cases:
            print(f"\n  [count=None 케이스 상세 — 첫 3개]")
            for case in none_cases[:3]:
                print(f"  slot={case['slot']} item={case['item'][:40]}")
                print(f"  ul_html: {case['ul_html'][:300]}")
                print()

        import asyncio
        import time
        time.sleep(3)  # 스펙 간 쿨다운


if __name__ == "__main__":
    main()
