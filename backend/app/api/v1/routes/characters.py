from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.repositories.character_repo import get_cached_character, upsert_character
from app.schemas.character import CharacterPublic
from app.services.blizzard import get_character_profile, get_realm_slug

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("/{realm}/{name}", response_model=CharacterPublic)
async def get_character(realm: str, name: str, session: SessionDep) -> CharacterPublic:
    # 1. Cache check (10분 이내면 DB 반환)
    cached = get_cached_character(session, realm, name)
    if cached:
        return CharacterPublic(
            id=cached.id,
            name=cached.name,
            realm=cached.realm,
            item_level=cached.item_level,
            last_synced_at=cached.last_synced_at,
            from_cache=True,
        )

    # 2. Cache miss → Blizzard API 호출
    realm_slug = get_realm_slug(realm)
    profile = await get_character_profile(realm_slug, name)

    if not profile:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없어요")

    character = upsert_character(
        session,
        {
            "name": profile.get("name", name),
            "realm": realm,
            "item_level": profile.get("equipped_item_level"),
            "blizzard_raw": profile,
        },
    )

    return CharacterPublic(
        id=character.id,
        name=character.name,
        realm=character.realm,
        item_level=character.item_level,
        last_synced_at=character.last_synced_at,
        from_cache=False,
    )
