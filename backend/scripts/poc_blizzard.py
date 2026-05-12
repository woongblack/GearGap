"""
Blizzard API PoC — OAuth 토큰 발급 + 캐릭터 장비 조회 검증

실행: backend/ 디렉토리에서
    python scripts/poc_blizzard.py <캐릭터명> <서버>

예시:
    python scripts/poc_blizzard.py 캐릭터이름 아즈샤라
"""
import asyncio
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# backend/ 를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from app.core.config import settings  # noqa: E402 — .env 로드 후 import
from app.services.blizzard import (  # noqa: E402
    _get_access_token,
    get_character_equipment,
    get_character_profile,
    get_realm_slug,
)

SLOT_NAMES_KR = {
    "HEAD": "머리",
    "NECK": "목",
    "SHOULDER": "어깨",
    "BACK": "등",
    "CHEST": "가슴",
    "SHIRT": "셔츠",
    "TABARD": "타바드",
    "WRIST": "손목",
    "HANDS": "손",
    "WAIST": "허리",
    "LEGS": "다리",
    "FEET": "발",
    "FINGER_1": "반지1",
    "FINGER_2": "반지2",
    "TRINKET_1": "장신구1",
    "TRINKET_2": "장신구2",
    "MAIN_HAND": "주무기",
    "OFF_HAND": "보조무기",
}


async def main(char_name: str, realm_kr: str) -> None:
    realm_slug = get_realm_slug(realm_kr)
    print(f"\n=== GearGap Blizzard API PoC ===")
    print(f"캐릭터: {char_name} @ {realm_kr} (slug: {realm_slug})")
    print(f"Region: {settings.BLIZZARD_REGION} | Namespace: {settings.BLIZZARD_NAMESPACE}\n")

    # Step 1: OAuth 토큰
    print("[1/3] OAuth 토큰 발급 중...")
    try:
        token = await _get_access_token()
        print(f"      OK — 토큰 앞 8자리: {token[:8]}...\n")
    except httpx.HTTPStatusError as e:
        print(f"      FAIL — {e.response.status_code}: {e.response.text}")
        return

    # Step 2: 캐릭터 프로필
    print("[2/3] 캐릭터 프로필 조회...")
    profile = await get_character_profile(realm_slug, char_name)
    if profile is None:
        print(f"      FAIL — 캐릭터를 찾을 수 없음 (realm={realm_slug}, name={char_name.lower()})")
        return

    level = profile.get("level", "?")
    ilvl = profile.get("average_item_level", "?")
    equipped_ilvl = profile.get("equipped_item_level", "?")
    cls = profile.get("character_class", {}).get("name", "?")
    spec = profile.get("active_spec", {}).get("name", "?")
    print(f"      OK — {char_name} | Lv.{level} {cls} ({spec})")
    print(f"      장착 아이템 레벨: {equipped_ilvl} | 평균 아이템 레벨: {ilvl}\n")

    # Step 3: 장비 18슬롯
    print("[3/3] 장비 조회...")
    equipment = await get_character_equipment(realm_slug, char_name)
    if equipment is None:
        print("      FAIL — 장비 정보를 가져올 수 없음")
        return

    items = equipment.get("equipped_items", [])
    print(f"      OK — {len(items)}개 슬롯\n")
    print(f"{'슬롯':<10} {'아이템 레벨':>8}  {'아이템명'}")
    print("-" * 55)
    for item in sorted(items, key=lambda x: x.get("slot", {}).get("type", "")):
        slot_type = item.get("slot", {}).get("type", "?")
        slot_kr = SLOT_NAMES_KR.get(slot_type, slot_type)
        item_name = item.get("name", "?")
        item_ilvl = item.get("level", {}).get("value", "?")
        item_id = item.get("item", {}).get("id", "?")
        print(f"{slot_kr:<10} {item_ilvl:>8}  {item_name}  (ID: {item_id})")

    print("\n=== PoC 완료 ===")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python scripts/poc_blizzard.py <캐릭터명> <서버명>")
        print("예시:   python scripts/poc_blizzard.py 워록이름 아즈샤라")
        sys.exit(1)

    char_name = sys.argv[1]
    realm_kr = sys.argv[2]
    asyncio.run(main(char_name, realm_kr))
