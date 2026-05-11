from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class WeightParams(BaseModel):
    w_dps: float = 1.0      # 0.5 ~ 2.0
    w_time: float = 1.0
    w_prob: float = 1.0


class EvidenceDetail(BaseModel):
    """근거 패널 (?) 클릭 시 표시되는 데이터"""
    dps_gain: Decimal
    dps_source: str             # e.g. "bloodmallet"
    dps_sim_date: str
    dps_sim_profile: str        # e.g. "patchwerk" → UI에서 "⚠️ 패치워크 기준" 표시
    avg_clear_minutes: int
    time_source: str
    drop_rate: Decimal
    drop_source: str
    formula: str                # "(dps_gain × W_dps) ÷ (avg_clear_minutes × W_time) × (drop_rate × W_prob)"


class EfficiencyCandidate(BaseModel):
    content_id: int
    content_name: str
    content_type: str
    difficulty: str
    item_id: int
    item_name: str
    item_name_kr: Optional[str]
    slot: str
    boss_name: Optional[str]
    efficiency_score: Decimal
    evidence: EvidenceDetail


class EfficiencyResponse(BaseModel):
    character_name: str
    spec_name: str
    patch_version: str
    weights: WeightParams
    candidates: list[EfficiencyCandidate]
