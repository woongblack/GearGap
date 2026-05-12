from typing import Any, Optional

from sqlalchemy import JSON
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
    wowhead_raw: Optional[Any] = Field(default=None, sa_column=SAColumn(JSON))


class Content(SQLModel, table=True):
    __tablename__ = "contents"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: str                           # "raid" | "mythic_plus"
    name_kr: str                        # e.g. "한밤의 요새"
    difficulty: str                     # "normal" | "heroic" | "mythic" | "M+10"
    patch_version: str = Field(foreign_key="patch_versions.version")
    is_active: bool = True


class DropSource(SQLModel, table=True):
    __tablename__ = "drop_sources"

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id")
    content_id: int = Field(foreign_key="contents.id")
    boss_name: Optional[str] = None
    item_level: Optional[int] = None
    patch_version: str = Field(foreign_key="patch_versions.version")
    is_active: bool = True
