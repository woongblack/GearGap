from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CharacterPublic(BaseModel):
    id: int
    name: str
    realm: str
    class_name: Optional[str] = None
    spec_name: Optional[str] = None
    item_level: Optional[int] = None
    last_synced_at: Optional[datetime] = None
    from_cache: bool = False


class CharacterStatsPublic(BaseModel):
    haste: Optional[int] = None
    crit: Optional[int] = None
    mastery: Optional[int] = None
    versatility: Optional[int] = None
