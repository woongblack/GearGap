from typing import Annotated, Literal, Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.api.deps import SessionDep
from app.repositories.character_repo import get_cached_character, upsert_character, upsert_equipment
from app.schemas.character import CharacterPublic
from app.schemas.roadmap import RoadmapOut
from app.services.blizzard import (
    extract_class_spec,
    get_character_equipment,
    get_character_profile,
    get_realm_slug,
    parse_equipment,
)
from app.services.roadmap import get_roadmap

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("/{realm}/{name}", response_model=CharacterPublic)
async def get_character(realm: str, name: str, session: SessionDep) -> CharacterPublic:
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


@router.get("/{realm}/{name}/roadmap", response_model=RoadmapOut)
async def get_character_roadmap(
    realm: str,
    name: str,
    session: SessionDep,
    content_type: Annotated[Literal["mythic-plus"], Query()] = "mythic-plus",
    spec_name: Annotated[Optional[str], Query()] = None,
) -> RoadmapOut:
    realm_slug = get_realm_slug(realm)

    cached = get_cached_character(session, realm, name)

    if cached:
        character = cached
    else:
        try:
            profile = await get_character_profile(realm_slug, name)
        except httpx.TimeoutException:
            raise HTTPException(status_code=502, detail="Blizzard API 응답 시간 초과")
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Blizzard API 오류")

        if not profile:
            raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없어요")

        try:
            equipment_raw = await get_character_equipment(realm_slug, name)
        except httpx.TimeoutException:
            raise HTTPException(status_code=502, detail="Blizzard API 응답 시간 초과")
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Blizzard API 오류")

        character = upsert_character(
            session,
            {
                "name": profile.get("name", name),
                "realm": realm,
                "item_level": profile.get("equipped_item_level"),
                "blizzard_raw": profile,
            },
        )

        if equipment_raw:
            try:
                upsert_equipment(session, character.id, parse_equipment(equipment_raw))
            except Exception as e:
                session.rollback()
                raise HTTPException(status_code=500, detail="장비 데이터 저장 중 오류가 발생했어요") from e

    # class_name / spec_name 추출
    blizzard_raw = character.blizzard_raw or {}
    class_name, active_spec = extract_class_spec(blizzard_raw)

    resolved_spec = spec_name if spec_name is not None else active_spec

    if not class_name or not resolved_spec:
        raise HTTPException(status_code=404, detail="캐릭터 클래스/스펙 정보를 가져올 수 없어요")

    try:
        return get_roadmap(session, character.id, class_name, resolved_spec, content_type)
    except ValueError:
        raise HTTPException(status_code=404, detail="DPS 스펙만 지원해요 (힐러/탱커 미지원)")
