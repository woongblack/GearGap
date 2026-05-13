import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

from sqlmodel import Session, delete, select

from app.constants.specs import DPS_SPECS
from app.models.popularity import SpecSlotItemPopularity
from app.services.murlok import MurlokScraper

logger = logging.getLogger(__name__)


@dataclass
class IngestionResult:
    total_rows: int = 0
    success_specs: list[tuple[str, str]] = field(default_factory=list)
    failed_specs: list[tuple[str, str, str]] = field(default_factory=list)  # (class, spec, error)
    duration_seconds: float = 0.0

    @property
    def exit_code(self) -> int:
        if not self.failed_specs:
            return 0
        if not self.success_specs:
            return 2
        return 1


async def ingest_single_spec(
    scraper: MurlokScraper,
    session: Session,
    class_name: str,
    spec_name: str,
    sync_start: datetime,
    content_type: str = "mythic-plus",
) -> int:
    """스펙 1개 ingestion — delete-and-insert, 스펙 단위 트랜잭션. 적재 행 수 반환."""
    items = await scraper.get_slot_popularity(class_name, spec_name, content_type)

    rows = [
        SpecSlotItemPopularity(
            class_name=class_name,
            spec_name=spec_name,
            content_type=content_type,
            slot=item.slot,
            item_id=item.item_id,
            item_name=item.item_name,
            count=item.count,
            total_sample=item.total_sample,
            scraped_at=sync_start,  # 사이클 시작 시각으로 통일
        )
        for item in items
    ]

    with session.begin():
        session.exec(
            delete(SpecSlotItemPopularity).where(
                SpecSlotItemPopularity.class_name == class_name,
                SpecSlotItemPopularity.spec_name == spec_name,
                SpecSlotItemPopularity.content_type == content_type,
            )
        )
        for row in rows:
            session.add(row)

    return len(rows)


async def ingest_all_specs(
    scraper: MurlokScraper,
    session: Session,
    specs: list[tuple[str, str]] | None = None,
    sleep_between: float = 10.0,
) -> IngestionResult:
    """DPS 전 스펙 순차 ingestion. 1개 실패해도 나머지 계속 진행."""
    if specs is None:
        specs = DPS_SPECS

    result = IngestionResult()
    sync_start = datetime.now(timezone.utc)
    wall_start = time.monotonic()
    total = len(specs)

    for i, (class_name, spec_name) in enumerate(specs, start=1):
        label = f"{class_name}/{spec_name}"
        print(f"[{i:>2}/{total}] {label:<36} ...", end="", flush=True)
        spec_start = time.monotonic()

        try:
            row_count = await ingest_single_spec(
                scraper, session, class_name, spec_name, sync_start
            )
            elapsed = time.monotonic() - spec_start
            print(f" OK  {row_count:>3} rows  ({elapsed:.1f}s)")
            result.total_rows += row_count
            result.success_specs.append((class_name, spec_name))

        except Exception as exc:
            elapsed = time.monotonic() - spec_start
            print(f" FAIL  ({elapsed:.1f}s)  {exc}")
            logger.exception("ingestion failed: %s/%s", class_name, spec_name)
            result.failed_specs.append((class_name, spec_name, str(exc)))

        if i < total:
            await asyncio.sleep(sleep_between)

    result.duration_seconds = time.monotonic() - wall_start
    return result
