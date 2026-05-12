"""
Blizzard Mythic+ Leaderboard API PoC
- 목표: 던전별 상위 플레이어 목록(realm/name) 확보 가능 여부 확인
- 확인 순서:
  1. 현재 M+ 시즌 정보 조회
  2. 연결 서버 ID 조회 (한국 아즈샤라)
  3. 던전 리더보드에서 상위 캐릭터 추출
"""
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import json

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from app.services.blizzard import _get_access_token
from app.core.config import settings

BASE = f"https://{settings.BLIZZARD_REGION}.api.blizzard.com"
STATIC_NS = f"static-{settings.BLIZZARD_REGION}"
DYNAMIC_NS = f"dynamic-{settings.BLIZZARD_REGION}"


async def get(client: httpx.AsyncClient, url: str, namespace: str) -> dict:
    token = await _get_access_token()
    r = await client.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params={"namespace": namespace, "locale": settings.BLIZZARD_LOCALE},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


async def main() -> None:
    print("=== Blizzard Mythic+ Leaderboard API PoC ===\n")

    async with httpx.AsyncClient() as client:
        # Step 1: 현재 M+ 시즌
        print("[1/4] M+ 시즌 인덱스 조회...")
        try:
            seasons = await get(client, f"{BASE}/data/wow/mythic-keystone/season/index", DYNAMIC_NS)
            current = seasons.get("current_season", {})
            season_id = current.get("id")
            print(f"      현재 시즌 ID: {season_id}")
        except Exception as e:
            print(f"      FAIL: {e}")
            return

        # Step 2: 던전 목록
        print("\n[2/4] M+ 던전 목록 조회...")
        try:
            dungeons = await get(client, f"{BASE}/data/wow/mythic-keystone/dungeon/index", DYNAMIC_NS)
            dungeon_list = dungeons.get("dungeons", [])[:5]  # 상위 5개만
            print(f"      총 {len(dungeons.get('dungeons', []))}개 던전 (상위 5개 표시)")
            for d in dungeon_list:
                print(f"      - [{d['id']}] {d['name']}")
        except Exception as e:
            print(f"      FAIL: {e}")
            return

        if not dungeon_list:
            print("던전 목록 없음")
            return

        # Step 3: 연결 서버 인덱스에서 아즈샤라 찾기
        print("\n[3/4] 연결 서버(아즈샤라) 조회...")
        try:
            realms = await get(client, f"{BASE}/data/wow/connected-realm/index", DYNAMIC_NS)
            connected_realm_urls = realms.get("connected_realms", [])
            print(f"      총 {len(connected_realm_urls)}개 연결 서버")

            # 첫 번째 서버로 리더보드 테스트 (아즈샤라 ID를 직접 시도)
            # 한국 아즈샤라는 보통 connected-realm ID 205 또는 비슷한 범위
            # 일단 첫 번째 URL에서 ID만 추출
            first_url = connected_realm_urls[0]["href"] if connected_realm_urls else None
            if first_url:
                realm_id = first_url.rstrip("/").split("/")[-1].split("?")[0]
                print(f"      첫 번째 연결 서버 ID: {realm_id} (테스트용)")
            else:
                realm_id = "205"
        except Exception as e:
            print(f"      FAIL: {e}")
            realm_id = "205"

        # Step 4: 리더보드 조회
        print(f"\n[4/4] 리더보드 조회 (connected-realm {realm_id}, 첫 번째 던전)...")
        dungeon_id = dungeon_list[0]["id"]
        dungeon_name = dungeon_list[0]["name"]

        try:
            # 기간(period) 인덱스 먼저 조회
            lb_index = await get(
                client,
                f"{BASE}/data/wow/connected-realm/{realm_id}/mythic-keystone/leaderboard/index",
                DYNAMIC_NS,
            )
            current_lb = lb_index.get("current_leaderboards", [])
            print(f"      현재 리더보드 항목 수: {len(current_lb)}")
            if current_lb:
                sample = current_lb[0]
                lb_url = sample["key"]["href"]
                print(f"      샘플 URL: {lb_url[:80]}...")

                # 실제 리더보드 데이터 조회
                lb_data = await get(client, lb_url.split("?")[0], DYNAMIC_NS)
                entries = lb_data.get("leading_groups", [])[:5]
                print(f"\n      상위 그룹 {len(entries)}개 (던전: {lb_data.get('map', {}).get('name', '?')}):")
                for entry in entries:
                    rank = entry.get("ranking", "?")
                    duration = entry.get("duration", 0) // 1000 // 60
                    keystone_level = entry.get("keystone_level", "?")
                    members = entry.get("members", [])
                    print(f"      {rank}위 | +{keystone_level} | {duration}분")
                    for m in members:
                        char = m.get("character", {})
                        realm = char.get("realm", {}).get("slug", "?")
                        name = char.get("name", "?")
                        spec = m.get("specialization", {}).get("name", "?")
                        cls = char.get("playable_class", {}).get("name", "?")
                        print(f"        - {name} @ {realm} | {cls} ({spec})")
        except Exception as e:
            print(f"      FAIL: {e}")
            import traceback
            traceback.print_exc()

    print("\n=== PoC 완료 ===")


if __name__ == "__main__":
    asyncio.run(main())
