"""Raider.IO 공개 API 엔드포인트 탐색"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import httpx

ENDPOINTS = [
    "https://raider.io/api/v1/mythic-plus/runs?season=season-tww-2&region=world&dungeon=all&affixes=all&page=0",
    "https://raider.io/api/v1/mythic-plus/leaderboards?season=season-tww-2&region=world&dungeon=all&limit=5",
    "https://raider.io/api/v1/mythic-plus/score-tiers?season=season-tww-2",
]

for url in ENDPOINTS:
    r = httpx.get(url, timeout=10, headers={"Accept": "application/json"})
    ct = r.headers.get("content-type", "")
    kind = "JSON" if "json" in ct else "HTML"
    print(f"[{r.status_code}] {kind} | {url[:75]}")
    if "json" in ct and r.status_code == 200:
        data = r.json()
        print(f"  keys: {list(data.keys())[:8]}")
        # runs 엔드포인트면 첫 번째 run의 roster 확인
        # runs 엔드포인트: rankings 키
        if "rankings" in data:
            rankings = data["rankings"]
            print(f"  rankings 수: {len(rankings)}")
            if rankings:
                first = rankings[0]
                print(f"  첫 번째 ranking keys: {list(first.keys())[:8]}")
                roster = first.get("run", {}).get("roster", [])
                if not roster:
                    roster = first.get("roster", [])
                print(f"  roster ({len(roster)}명):")
                for m in roster[:5]:
                    char = m.get("character", {})
                    name = char.get("name", "?")
                    realm = char.get("realm", {}).get("slug", "?")
                    region = char.get("region", {}).get("slug", "?")
                    spec = char.get("spec", {}).get("name", "?")
                    cls = char.get("class", {}).get("name", "?")
                    print(f"    - {name} @ {realm} ({region}) | {cls} {spec}")
    print()
