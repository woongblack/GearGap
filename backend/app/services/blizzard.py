from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import httpx

from app.core.config import settings

# Blizzard slot type → ssip canonical slot
# FINGER_1/2 → ring_1/ring_2, TRINKET_1/2 → trinket_1/trinket_2 (이중 슬롯 분리 저장)
BLIZZARD_SLOT_MAP: dict[str, str] = {
    "HEAD": "head",
    "NECK": "neck",
    "SHOULDER": "shoulders",
    "BACK": "back",
    "CHEST": "chest",
    "WRIST": "wrist",
    "HANDS": "hands",
    "WAIST": "waist",
    "LEGS": "legs",
    "FEET": "feet",
    "FINGER_1": "ring_1",
    "FINGER_2": "ring_2",
    "TRINKET_1": "trinket_1",
    "TRINKET_2": "trinket_2",
    "MAIN_HAND": "main_hand",
    "OFF_HAND": "off_hand",
}

_REALM_SLUGS: dict[str, str] = {
    "아즈샤라": "azshara",
    "줄진": "zul-jin",
    "하이잘": "hyjal",
    "데스윙": "deathwing",
    "헬스크림": "hellscream",
    "노르간논": "norgannon",
    "달라란": "dalaran",
    "세나리우스": "cenarius",
    "굴단": "gul-dan",
}

_token: Optional[str] = None
_token_expires_at: Optional[datetime] = None


def get_realm_slug(realm_kr: str) -> str:
    return _REALM_SLUGS.get(realm_kr, realm_kr.lower())


async def _get_access_token() -> str:
    global _token, _token_expires_at

    if _token and _token_expires_at and _token_expires_at > datetime.now(timezone.utc):
        return _token

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://oauth.battle.net/token",
            data={"grant_type": "client_credentials"},
            auth=(settings.BLIZZARD_CLIENT_ID, settings.BLIZZARD_CLIENT_SECRET),
        )
        res.raise_for_status()
        data = res.json()

    _token = data["access_token"]
    _token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=data["expires_in"] - 60)
    return _token


async def get_character_profile(realm_slug: str, name: str) -> Optional[dict[str, Any]]:
    token = await _get_access_token()
    url = f"https://{settings.BLIZZARD_REGION}.api.blizzard.com/profile/wow/character/{realm_slug}/{name.lower()}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params={"namespace": settings.BLIZZARD_NAMESPACE, "locale": settings.BLIZZARD_LOCALE},
        )

    if res.status_code == 404:
        return None
    res.raise_for_status()
    return res.json()


async def get_character_equipment(realm_slug: str, name: str) -> Optional[dict[str, Any]]:
    token = await _get_access_token()
    url = f"https://{settings.BLIZZARD_REGION}.api.blizzard.com/profile/wow/character/{realm_slug}/{name.lower()}/equipment"

    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params={"namespace": settings.BLIZZARD_NAMESPACE, "locale": settings.BLIZZARD_LOCALE},
        )

    if res.status_code == 404:
        return None
    res.raise_for_status()
    return res.json()


def parse_equipment(equipment_raw: dict[str, Any]) -> list[dict]:
    """Blizzard equipment API 응답 → character_equipment upsert용 slot dict 리스트."""
    slots = []
    for item in equipment_raw.get("equipped_items", []):
        blizzard_slot = item.get("slot", {}).get("type", "")
        canonical = BLIZZARD_SLOT_MAP.get(blizzard_slot)
        if canonical is None:
            continue  # SHIRT, TABARD 등 ssip에 없는 슬롯 무시
        slots.append({
            "slot": canonical,
            "item_id": item.get("item", {}).get("id"),
            "item_name": item.get("name"),
            "item_level": item.get("level", {}).get("value"),
        })
    return slots


def extract_class_spec(profile: dict[str, Any]) -> tuple[str, str]:
    """Blizzard profile → (class_name, spec_name) Murlok 슬러그 형식."""
    class_name = profile.get("character_class", {}).get("name", "")
    spec_name = profile.get("active_spec", {}).get("name", "")
    return (
        class_name.lower().replace(" ", "-"),
        spec_name.lower().replace(" ", "-"),
    )
