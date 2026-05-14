"""Raidbots ingestion CLI 진입점.

사용법:
    python scripts/run_raidbots_ingestion.py
    python scripts/run_raidbots_ingestion.py --dry-run
    python scripts/run_raidbots_ingestion.py --patch 12.0.5
"""
import argparse
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)

from app.core.db import engine
from app.workers.raidbots_ingestion import ingest
from sqlmodel import Session


def main() -> int:
    parser = argparse.ArgumentParser(description="Raidbots → GearGap DB ingestion")
    parser.add_argument("--dry-run", action="store_true", help="fetch만 하고 DB 쓰기 없음")
    parser.add_argument("--patch", default=None, help="패치 버전 (기본: CURRENT_PATCH_VERSION)")
    parser.add_argument("--no-sleep", action="store_true", help="throttle sleep 생략 (테스트용)")
    args = parser.parse_args()

    sleep = 0.0 if args.no_sleep else 10.0

    with Session(engine) as session:
        try:
            result = ingest(
                session,
                patch_version=args.patch,
                dry_run=args.dry_run,
                sleep_between=sleep,
            )
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
        except Exception as e:
            print(f"FATAL: {e}", file=sys.stderr)
            logging.exception("ingestion 실패")
            return 1

    if args.dry_run:
        return 0

    print(f"\n=== ingestion 완료 ===")
    print(f"  contents  : {result.inserted_contents}")
    print(f"  encounters: {result.inserted_encounters}")
    print(f"  items     : {result.inserted_items}")
    print(f"  drops     : {result.inserted_drops}")
    print(f"  skipped   : {result.skipped_drops}")
    print(f"  소요 시간  : {result.duration_seconds:.1f}s")
    return result.exit_code


if __name__ == "__main__":
    sys.exit(main())
