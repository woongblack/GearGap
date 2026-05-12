"""
검증 3단계
- Rings HTML 구조 상세 (Finger_1/2 분리 가능한지)
- OffHand 없는 스펙 패턴
- Murlok 슬롯명 전체 수집
- 26 DPS 스펙 스모크 테스트
"""
import io, sys, re, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}

# TWW 시즌 2 기준 26 DPS 스펙 (탱/힐 제외)
DPS_SPECS = [
    ("death-knight", "frost"),
    ("death-knight", "unholy"),
    ("demon-hunter", "havoc"),
    ("druid", "balance"),
    ("druid", "feral"),
    ("evoker", "devastation"),
    ("evoker", "augmentation"),
    ("hunter", "beast-mastery"),
    ("hunter", "marksmanship"),
    ("hunter", "survival"),
    ("mage", "arcane"),
    ("mage", "fire"),
    ("mage", "frost"),
    ("monk", "windwalker"),
    ("paladin", "retribution"),
    ("priest", "shadow"),
    ("rogue", "assassination"),
    ("rogue", "outlaw"),
    ("rogue", "subtlety"),
    ("shaman", "elemental"),
    ("shaman", "enhancement"),
    ("warlock", "affliction"),
    ("warlock", "demonology"),
    ("warlock", "destruction"),
    ("warrior", "arms"),
    ("warrior", "fury"),
]


def fetch_soup(cls: str, spec: str) -> BeautifulSoup | None:
    url = f"https://murlok.io/{cls}/{spec}/m+"
    try:
        r = httpx.get(url, timeout=15, headers=HEADERS, follow_redirects=True)
        if r.status_code != 200:
            return None, r.status_code
        return BeautifulSoup(r.text, "html.parser"), 200
    except Exception as e:
        return None, str(e)


def get_total_sample(soup: BeautifulSoup) -> int | None:
    for el in soup.find_all(string=re.compile(r'top\s+(\d+)', re.I)):
        m = re.search(r'top\s+(\d+)', el.strip(), re.I)
        if m:
            return int(m.group(1))
    return None


def get_slots(soup: BeautifulSoup) -> dict[str, list]:
    section = soup.find("section", class_="wow-equipment-slots")
    if not section:
        return {}
    slots = {}
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
            count = None
            ul = li.find("ul")
            if ul:
                for candidate in reversed(ul.find_all("li", recursive=False)):
                    for svg in candidate.find_all("svg"):
                        svg.decompose()
                    clean = candidate.get_text(strip=True)
                    m = re.search(r'^(\d+)$', clean)
                    if m:
                        count = int(m.group(1))
                        break
            items.append({"item_id": item_id, "name": item_name, "count": count})
        slots[slot_name] = items
    return slots


def main():
    # ── Part 1: Rings HTML 구조 상세 ──
    print("=" * 60)
    print("PART 1: Rings 슬롯 HTML 구조 상세 (warlock/destruction)")
    print("=" * 60)
    soup, status = fetch_soup("warlock", "destruction")
    if soup:
        section = soup.find("section", class_="wow-equipment-slots")
        for box in section.find_all("div", recursive=False):
            h3 = box.find("h3")
            if h3 and h3.text.strip() == "Rings":
                print(f"부모 div class: {box.get('class')}")
                print(f"조부모: {box.parent.name} class={box.parent.get('class')}")
                # h3 전후 siblings
                print(f"\nh3 형제 구조:")
                for i, sib in enumerate(box.children):
                    if hasattr(sib, 'name') and sib.name:
                        print(f"  [{i}] <{sib.name}> '{sib.text[:60].strip()}'")
                # ol 안 첫 두 li 출력
                ol = box.find("ol")
                print(f"\nol 직속 li 수: {len(ol.find_all('li', class_='vi-poppable', recursive=False))}")
                for li in ol.find_all("li", class_="vi-poppable", recursive=False)[:3]:
                    h4 = li.find("h4")
                    a = li.find("a", href=re.compile(r'wowhead'))
                    print(f"  item: {h4.text.strip() if h4 else '?'} | href: {a['href'] if a else '?'}")
                break

    # ── Part 2: 26 DPS 스펙 스모크 테스트 ──
    print("\n\n" + "=" * 60)
    print("PART 2: 26 DPS 스펙 스모크 테스트")
    print("=" * 60)
    print(f"{'스펙':<35} {'status':>6} {'sample':>7} {'슬롯':>5} {'아이템':>6} {'None수':>6} {'이상':>5}")
    print("-" * 70)

    all_slot_names = set()
    anomalies = []

    for cls, spec in DPS_SPECS:
        time.sleep(2)
        soup, status = fetch_soup(cls, spec)
        if soup is None:
            print(f"{cls}/{spec:<30} {str(status):>6}")
            anomalies.append((cls, spec, f"fetch fail: {status}"))
            continue

        sample = get_total_sample(soup)
        slots = get_slots(soup)
        slot_count = len(slots)
        item_count = sum(len(v) for v in slots.values())
        none_count = sum(1 for items in slots.values() for it in items if it["count"] is None)
        all_slot_names.update(slots.keys())

        is_anomaly = (
            sample != 50 or
            slot_count < 10 or
            none_count > 0
        )
        flag = "⚠️" if is_anomaly else "✅"

        print(f"{cls}/{spec:<30} {status:>6} {str(sample):>7} {slot_count:>5} {item_count:>6} {none_count:>6} {flag:>5}")

        if is_anomaly:
            anomalies.append((cls, spec, f"sample={sample} slots={slot_count} none={none_count}"))

    print("\n전체 슬롯명 수집:")
    for s in sorted(all_slot_names):
        print(f"  - {s}")

    if anomalies:
        print(f"\n⚠️  이상 케이스 {len(anomalies)}개:")
        for cls, spec, reason in anomalies:
            print(f"  {cls}/{spec}: {reason}")
    else:
        print("\n✅ 이상 없음")


if __name__ == "__main__":
    main()
