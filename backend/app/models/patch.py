from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class PatchVersion(SQLModel, table=True):
    __tablename__ = "patch_versions"

    version: str = Field(primary_key=True)  # e.g. "11.1.5"
    name_kr: str  # e.g. "한밤의 요새"
    season_number: int
    released_at: date
    is_current: bool = False
    notes: Optional[str] = None
