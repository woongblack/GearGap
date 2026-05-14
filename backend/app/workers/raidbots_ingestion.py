"""Raidbots ingestion worker — Content/Encounter/Item/DropSource 적재"""
import logging
import os
import time
from dataclasses import dataclass, field

from sqlmodel import Session, delete

from app.models.item import Content, DropSource, Encounter, Item
from app.models.patch import PatchVersion
from app.services.raidbots_fetcher import DropItemDTO, InstanceDTO, RaidbotsFetcher

logger = logging.getLogger(__name__)


@dataclass
class IngestionResult:
    inserted_contents: int = 0
    inserted_encounters: int = 0
    inserted_items: int = 0
    inserted_drops: int = 0
    skipped_drops: int = 0   # slot/quality None 또는 encounter lookup miss
    duration_seconds: float = 0.0
    dry_run: bool = False

    @property
    def exit_code(self) -> int:
        return 0


def ingest(
    session: Session,
    patch_version: str | None = None,
    dry_run: bool = False,
    sleep_between: float = 10.0,
) -> IngestionResult:
    """Raidbots → DB 전체 ingestion.

    - patch_version: None이면 CURRENT_PATCH_VERSION 환경변수 사용.
    - dry_run: True면 fetch만 하고 DB 쓰기 없음.
    - sleep_between: instances.json → equippable-items.json 사이 대기 시간(초).
    """
    pv = patch_version or os.environ.get("CURRENT_PATCH_VERSION")
    if not pv:
        raise RuntimeError("CURRENT_PATCH_VERSION 환경변수가 없음")

    result = IngestionResult(dry_run=dry_run)
    wall_start = time.monotonic()

    # ── 1. Fetch instances
    fetcher = RaidbotsFetcher()
    logger.info("[raidbots] fetch_instances 시작")
    instances: list[InstanceDTO] = fetcher.fetch_instances()
    valid_ids = {inst.raidbots_id for inst in instances}
    logger.info("[raidbots] instances: %d개 (dungeon/raid, 양수 ID)", len(instances))

    # ── 2. Throttle
    logger.info("[raidbots] %.0f초 대기 (Raidbots CDN 리밋 회피)...", sleep_between)
    time.sleep(sleep_between)

    # ── 3. Fetch drops
    logger.info("[raidbots] fetch_drops 시작")
    drops: list[DropItemDTO] = fetcher.fetch_drops(valid_ids)
    logger.info("[raidbots] drops: %d개 (아이템-encounter 쌍)", len(drops))

    if dry_run:
        result.duration_seconds = time.monotonic() - wall_start
        _print_dry_run_summary(instances, drops, pv)
        return result

    # ── 4. DB write (단일 트랜잭션)
    with session.begin():
        # PatchVersion 존재 확인 — 없으면 명확한 에러 (트랜잭션 롤백)
        db_pv = session.get(PatchVersion, pv)
        if db_pv is None:
            raise RuntimeError(
                f"patch_versions에 '{pv}' 없음. "
                "수동 INSERT 필요: scripts/insert_patch_version.py"
            )

        # DELETE (FK 역순, is_active=True만)
        session.exec(
            delete(DropSource).where(
                DropSource.patch_version == pv, DropSource.is_active == True  # noqa: E712
            )
        )
        session.exec(
            delete(Item).where(
                Item.patch_version == pv, Item.is_active == True  # noqa: E712
            )
        )
        session.exec(
            delete(Encounter).where(
                Encounter.patch_version == pv, Encounter.is_active == True  # noqa: E712
            )
        )
        session.exec(
            delete(Content).where(
                Content.patch_version == pv, Content.is_active == True  # noqa: E712
            )
        )

        # INSERT Content
        content_lookup: dict[int, int] = {}  # raidbots_id → db id
        for inst in instances:
            c = Content(
                raidbots_id=inst.raidbots_id,
                type=inst.type,
                name_en=inst.name_en,
                patch_version=pv,
            )
            session.add(c)
            session.flush()
            content_lookup[inst.raidbots_id] = c.id  # type: ignore[assignment]
        result.inserted_contents = len(content_lookup)

        # INSERT Encounter
        encounter_lookup: dict[int, int] = {}  # raidbots_id → db id
        for inst in instances:
            content_db_id = content_lookup[inst.raidbots_id]
            for enc in inst.encounters:
                e = Encounter(
                    raidbots_id=enc.raidbots_id,
                    content_id=content_db_id,
                    name=enc.name,
                    patch_version=pv,
                )
                session.add(e)
                session.flush()
                encounter_lookup[enc.raidbots_id] = e.id  # type: ignore[assignment]
        result.inserted_encounters = len(encounter_lookup)

        # INSERT Item (item_id 단위 중복 제거)
        valid_drops = [d for d in drops if d.slot is not None and d.quality is not None]
        skipped_slot_quality = len(drops) - len(valid_drops)

        seen_item_ids: set[int] = set()
        for drop in valid_drops:
            if drop.item_id in seen_item_ids:
                continue
            seen_item_ids.add(drop.item_id)
            session.add(Item(
                id=drop.item_id,
                name=drop.name,
                slot=drop.slot.value,
                quality=drop.quality,
                base_item_level=drop.base_item_level or 0,
                patch_version=pv,
            ))
        session.flush()
        result.inserted_items = len(seen_item_ids)

        # INSERT DropSource
        seen_drop_keys: set[tuple[int, int]] = set()
        skipped_enc_miss = 0
        for drop in valid_drops:
            if drop.item_id not in seen_item_ids:
                continue
            enc_db_id = encounter_lookup.get(drop.encounter_raidbots_id)
            if enc_db_id is None:
                logger.warning(
                    "encounter lookup miss: raidbots_id=%d item=%r",
                    drop.encounter_raidbots_id, drop.name,
                )
                skipped_enc_miss += 1
                continue
            key = (drop.item_id, enc_db_id)
            if key in seen_drop_keys:
                continue
            seen_drop_keys.add(key)
            session.add(DropSource(
                item_id=drop.item_id,
                encounter_id=enc_db_id,
                patch_version=pv,
            ))
        result.inserted_drops = len(seen_drop_keys)
        result.skipped_drops = skipped_slot_quality + skipped_enc_miss

    result.duration_seconds = time.monotonic() - wall_start
    logger.info(
        "[raidbots] 완료 | contents=%d encounters=%d items=%d drops=%d skipped=%d (%.1fs)",
        result.inserted_contents, result.inserted_encounters,
        result.inserted_items, result.inserted_drops,
        result.skipped_drops, result.duration_seconds,
    )
    return result


def _print_dry_run_summary(
    instances: list[InstanceDTO],
    drops: list[DropItemDTO],
    patch_version: str,
) -> None:
    valid_drops = [d for d in drops if d.slot is not None and d.quality is not None]
    unique_items = len({d.item_id for d in valid_drops})
    skipped = len(drops) - len(valid_drops)
    print(f"[DRY-RUN] patch={patch_version}")
    print(f"  contents  : {len(instances)}")
    print(f"  encounters: {sum(len(i.encounters) for i in instances)}")
    print(f"  items     : {unique_items}")
    print(f"  drops     : {len(valid_drops)}")
    print(f"  skipped   : {skipped} (slot/quality None)")
