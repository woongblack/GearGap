from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlmodel import Session, select

from app.core.config import settings
from app.models.character import Character, CharacterEquipment, CharacterStats


def get_cached_character(session: Session, realm: str, name: str) -> Optional[Character]:
    character = session.exec(
        select(Character).where(Character.realm == realm, Character.name == name)
    ).first()

    if not character or not character.last_synced_at:
        return None

    age = datetime.now(timezone.utc) - character.last_synced_at.replace(tzinfo=timezone.utc)
    if age > timedelta(seconds=settings.CHARACTER_CACHE_TTL):
        return None

    return character


def upsert_character(session: Session, data: dict) -> Character:
    existing = session.exec(
        select(Character).where(
            Character.realm == data["realm"],
            Character.name == data["name"],
        )
    ).first()

    if existing:
        for key, value in data.items():
            setattr(existing, key, value)
        existing.last_synced_at = datetime.now(timezone.utc)
        session.add(existing)
    else:
        character = Character(**data, last_synced_at=datetime.now(timezone.utc))
        session.add(character)
        existing = character

    session.commit()
    session.refresh(existing)
    return existing


def upsert_equipment(session: Session, character_id: int, slots: list[dict]) -> None:
    for slot_data in slots:
        existing = session.exec(
            select(CharacterEquipment).where(
                CharacterEquipment.character_id == character_id,
                CharacterEquipment.slot == slot_data["slot"],
            )
        ).first()

        if existing:
            for key, value in slot_data.items():
                setattr(existing, key, value)
            session.add(existing)
        else:
            session.add(CharacterEquipment(character_id=character_id, **slot_data))

    session.commit()
