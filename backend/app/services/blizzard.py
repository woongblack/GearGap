from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import httpx

from app.core.config import settings

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

    async with httpx.AsyncClient() as client:
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

    async with httpx.AsyncClient() as client:
        res = await client.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            params={"namespace": settings.BLIZZARD_NAMESPACE, "locale": settings.BLIZZARD_LOCALE},
        )

    if res.status_code == 404:
        return None
    res.raise_for_status()
    return res.json()
