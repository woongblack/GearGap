from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Index, String, UniqueConstraint
from sqlmodel import Field, SQLModel

from app.services.murlok import Slot


class SpecSlotItemPopularity(SQLModel, table=True):
    __tablename__ = "spec_slot_item_popularity"
    __table_args__ = (
        Index("ix_ssip_lookup", "class_name", "spec_name", "content_type", "slot"),
        UniqueConstraint(
            "class_name", "spec_name", "content_type", "slot", "item_id",
            name="uq_ssip_item",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    class_name: str = Field(max_length=20)      # e.g. "warlock"
    spec_name: str = Field(max_length=20)        # e.g. "destruction"
    content_type: str = Field(max_length=20)     # "mythic-plus" | "raid"
    slot: Slot = Field(sa_column=Column(String(20), nullable=False))
    item_id: int
    item_name: str = Field(max_length=100)
    count: int                                   # 상위 50명 중 착용 수
    total_sample: int                            # 항상 50 (Murlok 기준)
    scraped_at: datetime
