"""
Raider.IO API PoC — M+ 랭킹 엔드포인트 확인

실행: backend/ 디렉토리에서
    python scripts/poc_raiderio.py
"""
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx

BASE = "https://raider.io/api/v1/mythic-plus/rankings/characters"
SEASONS = ["season-tww-2", "season-tww-1"]
SPECS = [
    ("warlock", "destruction"),
    ("warlock", "affliction"),
    ("warlock", "demonology"),
]


def check_rankings(season: str, cls: str, spec: str) -> None:
    url = f"{BASE}?region=world&season={season}&class={cls}&spec={spec}&limit=5"
    r = httpx.get(url, timeout=10)
    print(f"  status={r.status_code}  url={url}")
    if r.status_code != 200:
        print(f"  오류: {r.text[:300]}")
        return

    print(f"  raw 응답 앞 200자: {r.text[:200]}")
    try:
        data = r.json()
    except Exception as e:
        print(f"  JSON 파싱 실패: {e}")
        return
    ranked = data.get("rankings", {}).get("rankedCharacters", [])
    print(f"  rankedCharacters 수: {len(ranked)}")
    for i, entry in enumerate(ranked[:3], 1):
        char = entry.get("character", {})
        name = char.get("name", "?")
        realm = char.get("realm", {}).get("slug", "?")
        score = entry.get("score", "?")
        region = char.get("region", {}).get("slug", "?")
        print(f"  {i}위: {name} @ {realm} ({region}) — score {score}")


def main() -> None:
    print("=== Raider.IO M+ 랭킹 API PoC ===\n")

    active_season = None
    for season in SEASONS:
        print(f"[시즌 확인] {season}")
        url = f"{BASE}?region=world&season={season}&class=warlock&spec=destruction&limit=1"
        r = httpx.get(url, timeout=10)
        print(f"  status={r.status_code}")
        if r.status_code == 200:
            active_season = season
            print(f"  -> 활성 시즌 확인: {season}\n")
            break
        else:
            print(f"  -> {r.text[:150]}\n")

    if not active_season:
        print("활성 시즌을 찾지 못했습니다.")
        return

    print(f"=== 흑마법사 3개 스펙 상위 5명 조회 (시즌: {active_season}) ===\n")
    for cls, spec in SPECS:
        print(f"[{cls} / {spec}]")
        check_rankings(active_season, cls, spec)
        print()

    # realm/name 포함 여부 상세 확인
    print("=== 필드 구조 상세 확인 (destruction 1위) ===")
    url = f"{BASE}?region=world&season={active_season}&class=warlock&spec=destruction&limit=1"
    r = httpx.get(url, timeout=10)
    data = r.json()
    ranked = data.get("rankings", {}).get("rankedCharacters", [])
    if ranked:
        import json
        print(json.dumps(ranked[0], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
