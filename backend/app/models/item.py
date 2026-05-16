from typing import Any, Optional

from sqlalchemy import JSON, UniqueConstraint
from sqlalchemy import Column as SAColumn
from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: int = Field(primary_key=True)   # Blizzard item ID
    name: str
    name_kr: Optional[str] = None
    slot: str                           # e.g. "trinket", "ring"
    base_item_level: int
    quality: str                        # "epic" | "rare"
    patch_version: str = Field(foreign_key="patch_versions.version")
    is_active: bool = True
    icon_url: Optional[str] = None
    wowhead_raw: Optional[Any] = Field(default=None, sa_column=SAColumn(JSON))


class Content(SQLModel, table=True):
    __tablename__ = "contents"

    id: Optional[int] = Field(default=None, primary_key=True)
    raidbots_id: int = Field(unique=True)   # instances.json id (양수만 저장)
    type: str                               # "raid" | "dungeon"
                                            # ※ spec_slot_item_popularity.content_type("mythic-plus")와 별개 개념
    name_en: str                            # instances.json name (영문)
    name_kr: Optional[str] = None          # nullable (수동 입력용)
    patch_version: str = Field(foreign_key="patch_versions.version")
    is_active: bool = True


class Encounter(SQLModel, table=True):
    __tablename__ = "encounters"

    id: Optional[int] = Field(default=None, primary_key=True)
    raidbots_id: int = Field(unique=True)   # instances.json encounter.id
    content_id: int = Field(foreign_key="contents.id")
    name: str                               # e.g. "Forgemaster Garfrost"
    name_kr: Optional[str] = None
    patch_version: str = Field(foreign_key="patch_versions.version")
    is_active: bool = True


class DropSource(SQLModel, table=True):
    __tablename__ = "drop_sources"

    __table_args__ = (
        UniqueConstraint("item_id", "encounter_id", name="uq_dropsource_item_encounter"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id")
    encounter_id: int = Field(foreign_key="encounters.id")
    item_level: Optional[int] = None
    patch_version: str = Field(foreign_key="patch_versions.version")
    is_active: bool = True
