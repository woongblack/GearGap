from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class DropSourceOut(BaseModel):
    instance_name: str
    encounter_name: str
    item_level: Optional[int] = None  # difficulty 대리값


class BisCandidateOut(BaseModel):
    item_id: int
    item_name: str  # COALESCE(items.name, ssip.item_name)
    icon_url: Optional[str] = None
    count: int
    total_sample: int  # 항상 50 (Murlok 기준)
    source_type: Literal["drop", "unknown"]
    drop_sources: list[DropSourceOut]  # source_type="unknown"이면 []


class SlotRoadmapOut(BaseModel):
    slot: str
    my_item_id: Optional[int] = None
    my_item_name: Optional[str] = None   # items 테이블에 없으면 None
    my_item_level: Optional[int] = None
    is_bis: bool  # my_item_id == bis_candidates[0].item_id (source_type 무관)
    bis_candidates: list[BisCandidateOut]  # count DESC, 전체 반환 (UI에서 Top N 잘라냄)


class RoadmapOut(BaseModel):
    character_id: int
    class_name: str
    spec_name: str
    content_type: str
    scraped_at: Optional[datetime] = None  # ssip 최신 scraped_at
    slots: list[SlotRoadmapOut]  # 슬롯 알파벳 정렬
