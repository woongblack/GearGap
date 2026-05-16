from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from sqlalchemy import text
from sqlmodel import Session


@dataclass
class EquipmentRow:
    slot: str
    item_id: Optional[int]
    item_level: Optional[int]
    item_name: Optional[str]


@dataclass
class BisRow:
    slot: str
    item_id: int
    item_name: str
    icon_url: Optional[str]
    count: int
    total_sample: int
    scraped_at: Optional[datetime]
    source_type: str
    instance_name: Optional[str]
    encounter_name: Optional[str]
    drop_item_level: Optional[int]


def get_equipment_map(session: Session, character_id: int) -> dict[str, EquipmentRow]:
    rows = session.exec(
        text("""
            SELECT ce.slot, ce.item_id, ce.item_level, COALESCE(i.name, ce.item_name) AS item_name
            FROM character_equipment ce
            LEFT JOIN items i ON ce.item_id = i.id
            WHERE ce.character_id = :character_id
        """),
        params={"character_id": character_id},
    ).fetchall()

    return {
        row.slot: EquipmentRow(
            slot=row.slot,
            item_id=row.item_id,
            item_level=row.item_level,
            item_name=row.item_name,
        )
        for row in rows
    }


def get_bis_rows(
    session: Session,
    class_name: str,
    spec_name: str,
    content_type: str,
) -> list[BisRow]:
    rows = session.exec(
        text("""
            SELECT
                ssip.slot,
                ssip.item_id,
                COALESCE(i.name, ssip.item_name) AS item_name,
                i.icon_url,
                ssip.count,
                ssip.total_sample,
                ssip.scraped_at,
                CASE WHEN i.id IS NOT NULL THEN 'drop' ELSE 'unknown' END AS source_type,
                COALESCE(c.name_kr, c.name_en) AS instance_name,
                COALESCE(e.name_kr, e.name)   AS encounter_name,
                ds.item_level  AS drop_item_level
            FROM spec_slot_item_popularity ssip
            LEFT JOIN items i        ON ssip.item_id    = i.id        AND i.is_active  = 1
            LEFT JOIN drop_sources ds ON ds.item_id     = i.id        AND ds.is_active = 1
            LEFT JOIN encounters e   ON ds.encounter_id = e.id        AND e.is_active  = 1
            LEFT JOIN contents c     ON e.content_id    = c.id        AND c.is_active  = 1
            WHERE ssip.class_name   = :class_name
              AND ssip.spec_name    = :spec_name
              AND ssip.content_type = :content_type
            ORDER BY ssip.slot, ssip.count DESC, ds.item_level DESC
        """),
        params={
            "class_name": class_name,
            "spec_name": spec_name,
            "content_type": content_type,
        },
    ).fetchall()

    return [
        BisRow(
            slot=row.slot,
            item_id=row.item_id,
            item_name=row.item_name,
            icon_url=row.icon_url,
            count=row.count,
            total_sample=row.total_sample,
            scraped_at=row.scraped_at,
            source_type=row.source_type,
            instance_name=row.instance_name,
            encounter_name=row.encounter_name,
            drop_item_level=row.drop_item_level,
        )
        for row in rows
    ]
