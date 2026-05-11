from datetime import datetime
from typing import Any, Optional

from sqlalchemy import JSON
from sqlalchemy import Column as SAColumn
from sqlmodel import Field, SQLModel


class Character(SQLModel, table=True):
    __tablename__ = "characters"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    realm: str = Field(index=True)
    class_id: Optional[int] = Field(default=None, foreign_key="classes.id")
    active_spec_id: Optional[int] = Field(default=None, foreign_key="specs.id")
    item_level: Optional[int] = None
    blizzard_raw: Optional[Any] = Field(default=None, sa_column=SAColumn(JSON))
    last_synced_at: Optional[datetime] = None


class CharacterEquipment(SQLModel, table=True):
    __tablename__ = "character_equipment"

    id: Optional[int] = Field(default=None, primary_key=True)
    character_id: int = Field(foreign_key="characters.id")
    slot: str                   # e.g. "head", "trinket1"
    item_id: Optional[int] = Field(default=None, foreign_key="items.id")
    item_level: Optional[int] = None
    bonuses: Optional[Any] = Field(default=None, sa_column=SAColumn(JSON))
    synced_at: Optional[datetime] = None


class CharacterStats(SQLModel, table=True):
    __tablename__ = "character_stats"

    id: Optional[int] = Field(default=None, primary_key=True)
    character_id: int = Field(foreign_key="characters.id")
    haste: Optional[int] = None
    crit: Optional[int] = None
    mastery: Optional[int] = None
    versatility: Optional[int] = None
    synced_at: Optional[datetime] = None
