from datetime import date
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import JSON, Numeric
from sqlalchemy import Column as SAColumn
from sqlmodel import Field, SQLModel


class SimulationResult(SQLModel, table=True):
    __tablename__ = "simulation_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id")
    spec_id: int = Field(foreign_key="specs.id")
    dps_gain: Decimal = Field(sa_column=SAColumn(Numeric(precision=10, scale=2)))  # DPS Gain — 효율 점수 분자
    sim_profile: str = "patchwerk"      # 근거 패널에 "패치워크 기준 ⚠️" 표시용
    source: str = "bloodmallet"
    patch_version: str = Field(foreign_key="patch_versions.version")
    sim_date: date
    is_latest: bool = True              # 동일 패치 내 최신 시뮬 여부 (is_active와 구분)
    raw_data: Optional[Any] = Field(default=None, sa_column=SAColumn(JSON))
