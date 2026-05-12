"""
Raider.IO runs API — 클래스/스펙 필터 + 착용률 집계 가능성 검증

목표:
1. class=warlock 필터 파라미터 존재 여부 확인
2. 한국 서버(region=kr) 필터 가능 여부 확인
3. realm/name 필드로 Blizzard API 연계 가능 여부 확인
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx, json

BASE = "https://raider.io/api/v1/mythic-plus/runs"
SEASON = "season-tww-2"


def fetch_runs(region: str = "world", class_slug: str | None = None, spec_slug: str | None = None, limit: int = 10) -> list:
    params = f"season={SEASON}&region={region}&dungeon=all&affixes=all&page=0"
    url = f"{BASE}?{params}"
    r = httpx.get(url, timeout=10, headers={"Accept": "application/json"})
    if r.status_code != 200 or "json" not in r.headers.get("content-type", ""):
        print(f"  FAIL status={r.status_code}")
        return []
    data = r.json()
    rankings = data.get("rankings", [])

    # 클라이언트 사이드 필터 (class/spec)
    results = []
    for entry in rankings:
        roster = entry.get("run", {}).get("roster", [])
        for m in roster:
            char = m.get("character", {})
            cls = char.get("class", {}).get("slug", "")
            spec = char.get("spec", {}).get("slug", "")
            if class_slug and cls != class_slug:
                continue
            if spec_slug and spec != spec_slug:
                continue
            results.append({
                "name": char.get("name"),
                "realm": char.get("realm", {}).get("slug"),
                "region": char.get("region", {}).get("slug"),
                "class": char.get("class", {}).get("name"),
                "spec": char.get("spec", {}).get("name"),
                "score": entry.get("score"),
                "rank": entry.get("rank"),
            })
    return results[:limit]


def main() -> None:
    print("=== Raider.IO runs API 필터 검증 ===\n")

    # 1. 전체 (필터 없음) — slug 구조 확인
    print("[1] 전체 상위 run에서 roster 샘플 (slug 필드 확인)")
    r = httpx.get(f"{BASE}?season={SEASON}&region=world&dungeon=all&affixes=all&page=0", timeout=10)
    data = r.json()
    first_run = data["rankings"][0]["run"]
    first_member = first_run["roster"][0]["character"]
    print(f"  character 필드 키: {list(first_member.keys())}")
    print(f"  class 구조: {first_member.get('class')}")
    print(f"  spec 구조: {first_member.get('spec')}")
    print(f"  realm 구조: {first_member.get('realm')}")
    print()

    # 2. 흑마법사(warlock) 파멸(destruction) 필터
    print("[2] warlock destruction 필터 (world)")
    warlocks = fetch_runs(region="world", class_slug="warlock", spec_slug="destruction")
    print(f"  상위 20개 런 중 warlock/destruction: {len(warlocks)}명")
    for w in warlocks:
        print(f"  - {w['name']} @ {w['realm']} ({w['region']}) | {w['class']} {w['spec']} score={w['score']}")
    print()

    # 3. 한국 서버 필터
    print("[3] 한국 서버 (region=kr) 필터")
    kr_runs = fetch_runs(region="kr")
    print(f"  KR 상위 런 캐릭터 수: {len(kr_runs)}")
    for w in kr_runs[:5]:
        print(f"  - {w['name']} @ {w['realm']} ({w['region']}) | {w['class']} {w['spec']}")
    print()

    # 4. 결론 — Blizzard API 연계 가능 여부
    print("[4] Blizzard API 연계 가능 여부 확인")
    print("  realm.slug + character.name → Blizzard /profile/wow/character/{realm}/{name}/equipment")
    if warlocks:
        sample = warlocks[0]
        print(f"  예시 URL: https://kr.api.blizzard.com/profile/wow/character/{sample['realm']}/{sample['name'].lower()}/equipment")
    print()
    print("=== 완료 ===")


if __name__ == "__main__":
    main()
