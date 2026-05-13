"""
Murlok BiS ingestion CLI 진입점.

Usage:
    python scripts/run_murlok_ingestion.py [--dry-run] [--sleep SECONDS]

Options:
    --dry-run        DB 적재 없이 스크레이핑만 확인
    --sleep SECONDS  스펙 간 딜레이 (기본 10초)
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path

# backend/ 루트를 sys.path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.db import engine
from app.services.murlok import MurlokScraper
from app.workers.murlok_ingestion import ingest_all_specs
from sqlmodel import Session

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s  %(name)s  %(message)s",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Murlok BiS ingestion")
    parser.add_argument("--dry-run", action="store_true", help="스크레이핑만, DB 적재 없음")
    parser.add_argument("--sleep", type=float, default=10.0, metavar="SECONDS",
                        help="스펙 간 딜레이 (기본 10s)")
    return parser.parse_args()


async def main() -> int:
    args = parse_args()

    if args.dry_run:
        print("[DRY RUN] DB 적재 없이 첫 스펙만 스크레이핑 확인합니다.")
        scraper = MurlokScraper()
        items = await scraper.get_slot_popularity("warlock", "destruction")
        print(f"  warlock/destruction: {len(items)} items parsed")
        for item in items[:3]:
            print(f"    {item.slot:<14} {item.item_name} ({item.count}/{item.total_sample})")
        return 0

    scraper = MurlokScraper()
    with Session(engine) as session:
        result = await ingest_all_specs(scraper, session, sleep_between=args.sleep)

    mins, secs = divmod(int(result.duration_seconds), 60)
    print(f"\n{'='*55}")
    print(f"완료  총 {result.total_rows:,}행  {mins}m {secs}s")
    print(f"성공 {len(result.success_specs)}/{len(result.success_specs) + len(result.failed_specs)} 스펙")

    if result.failed_specs:
        print("\n실패 목록:")
        for cls, spec, err in result.failed_specs:
            print(f"  {cls}/{spec}: {err}")

    return result.exit_code


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
