from decimal import Decimal

from sqlmodel import Session, select

from app.models.item import Content, DropSource, Item
from app.models.simulation import SimulationResult
from app.schemas.efficiency import (
    EfficiencyCandidate,
    EfficiencyResponse,
    EvidenceDetail,
    WeightParams,
)


def calculate_efficiency_score(
    dps_gain: Decimal,
    avg_clear_minutes: int,
    drop_rate: Decimal,
    weights: WeightParams,
) -> Decimal:
    """
    효율 점수 = (dps_gain × W_dps) ÷ (avg_clear_minutes × W_time) × (drop_rate × W_prob)
    """
    if avg_clear_minutes == 0:
        return Decimal(0)
    return (
        (dps_gain * Decimal(str(weights.w_dps)))
        / (Decimal(avg_clear_minutes) * Decimal(str(weights.w_time)))
        * (drop_rate * Decimal(str(weights.w_prob)))
    )


def get_efficiency_candidates(
    session: Session,
    spec_id: int,
    patch_version: str,
    weights: WeightParams,
) -> list[EfficiencyCandidate]:
    # Active items for current patch
    items = session.exec(
        select(Item).where(Item.patch_version == patch_version, Item.is_active == True)
    ).all()

    candidates: list[EfficiencyCandidate] = []

    for item in items:
        sim = session.exec(
            select(SimulationResult).where(
                SimulationResult.item_id == item.id,
                SimulationResult.spec_id == spec_id,
                SimulationResult.patch_version == patch_version,
                SimulationResult.is_latest == True,
            )
        ).first()

        if not sim:
            continue

        drop_sources = session.exec(
            select(DropSource).where(
                DropSource.item_id == item.id,
                DropSource.patch_version == patch_version,
                DropSource.is_active == True,
            )
        ).all()

        for drop in drop_sources:
            content = session.get(Content, drop.content_id)
            if not content or not content.is_active:
                continue

            score = calculate_efficiency_score(
                sim.dps_gain, content.avg_clear_minutes, drop.drop_rate, weights
            )

            candidates.append(
                EfficiencyCandidate(
                    content_id=content.id,
                    content_name=content.name_kr,
                    content_type=content.type,
                    difficulty=content.difficulty,
                    item_id=item.id,
                    item_name=item.name,
                    item_name_kr=item.name_kr,
                    slot=item.slot,
                    boss_name=drop.boss_name,
                    efficiency_score=score,
                    evidence=EvidenceDetail(
                        dps_gain=sim.dps_gain,
                        dps_source=sim.source,
                        dps_sim_date=str(sim.sim_date),
                        dps_sim_profile=sim.sim_profile,
                        avg_clear_minutes=content.avg_clear_minutes,
                        time_source=content.source,
                        drop_rate=drop.drop_rate,
                        drop_source="wowhead",
                        formula="(dps_gain × W_dps) ÷ (avg_clear_minutes × W_time) × (drop_rate × W_prob)",
                    ),
                )
            )

    # 정렬은 허용, 순위(1위/2위) 강조는 UI에서 절대 금지
    candidates.sort(key=lambda c: c.efficiency_score, reverse=True)
    return candidates
