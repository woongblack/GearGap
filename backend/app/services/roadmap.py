from typing import Optional

from sqlmodel import Session

from app.constants.specs import DPS_SPECS
from app.repositories.roadmap_repo import BisRow, EquipmentRow, get_bis_rows, get_equipment_map
from app.schemas.roadmap import (
    BisCandidateOut,
    DropSourceOut,
    RoadmapOut,
    SlotRoadmapOut,
)

# ssip 슬롯 → DB에 분리 저장된 슬롯 키 (이중 슬롯)
_DUAL_SLOTS: dict[str, list[str]] = {
    "rings":    ["ring_1", "ring_2"],
    "trinkets": ["trinket_1", "trinket_2"],
}


def get_roadmap(
    session: Session,
    character_id: int,
    class_name: str,
    spec_name: str,
    content_type: str = "mythic-plus",
) -> RoadmapOut:
    if (class_name, spec_name) not in DPS_SPECS:
        raise ValueError("non_dps_spec")

    equipment_map = get_equipment_map(session, character_id)
    bis_rows = get_bis_rows(session, class_name, spec_name, content_type)

    bis_by_slot = _aggregate_bis(bis_rows)

    scraped_at = bis_rows[0].scraped_at if bis_rows else None

    slots = []
    for slot in sorted(bis_by_slot):
        candidates = bis_by_slot[slot]
        top_item_id = candidates[0].item_id if candidates else None

        if slot in _DUAL_SLOTS:
            slot_out = _build_dual_slot(slot, candidates, top_item_id, equipment_map)
        else:
            eq = equipment_map.get(slot)
            my_item_id = eq.item_id if eq else None
            slot_out = SlotRoadmapOut(
                slot=slot,
                my_item_id=my_item_id,
                my_item_name=eq.item_name if eq else None,
                my_item_level=eq.item_level if eq else None,
                is_bis=(my_item_id is not None and my_item_id == top_item_id),
                bis_candidates=candidates,
            )

        slots.append(slot_out)

    return RoadmapOut(
        character_id=character_id,
        class_name=class_name,
        spec_name=spec_name,
        content_type=content_type,
        scraped_at=scraped_at,
        slots=slots,
    )


def _build_dual_slot(
    slot: str,
    candidates: list[BisCandidateOut],
    top_item_id: Optional[int],
    equipment_map: dict[str, EquipmentRow],
) -> SlotRoadmapOut:
    """ring_1/ring_2 또는 trinket_1/trinket_2 중 하나라도 BiS면 is_bis=True.
    my_item_id: BiS 매칭된 슬롯 우선, 없으면 첫 번째 슬롯."""
    db_keys = _DUAL_SLOTS[slot]
    eqs = [equipment_map.get(k) for k in db_keys]

    matched = next(
        (eq for eq in eqs if eq and top_item_id and eq.item_id == top_item_id),
        None,
    )
    displayed = matched or next((eq for eq in eqs if eq), None)

    return SlotRoadmapOut(
        slot=slot,
        my_item_id=displayed.item_id if displayed else None,
        my_item_name=displayed.item_name if displayed else None,
        my_item_level=displayed.item_level if displayed else None,
        is_bis=matched is not None,
        bis_candidates=candidates,
    )


def _aggregate_bis(rows: list[BisRow]) -> dict[str, list[BisCandidateOut]]:
    # slot → {item_id → candidate} 순서 보존 dict (count DESC 이미 정렬됨)
    slot_acc: dict[str, dict[int, BisCandidateOut]] = {}

    for row in rows:
        if row.slot not in slot_acc:
            slot_acc[row.slot] = {}

        acc = slot_acc[row.slot]

        if row.item_id not in acc:
            # 첫 row에서만 count/total_sample/source_type 읽기
            acc[row.item_id] = BisCandidateOut(
                item_id=row.item_id,
                item_name=row.item_name,
                icon_url=row.icon_url,
                count=row.count,
                total_sample=row.total_sample,
                source_type=row.source_type,
                drop_sources=[],
            )

        # 이후 같은 item_id row는 drop_sources만 append
        if row.encounter_name:
            acc[row.item_id].drop_sources.append(
                DropSourceOut(
                    instance_name=row.instance_name or "",
                    encounter_name=row.encounter_name,
                    item_level=row.drop_item_level,
                )
            )

    return {slot: list(items.values()) for slot, items in slot_acc.items()}
