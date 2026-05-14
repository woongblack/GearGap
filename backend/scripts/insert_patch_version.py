"""patch_versions 수동 INSERT — 12.0.5 Midnight Season 1"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, select

load_dotenv()

from app.models.patch import PatchVersion
from app.core.db import engine

with Session(engine) as session:
    existing = session.get(PatchVersion, "12.0.5")
    if existing:
        print("이미 존재: version=12.0.5")
        print(f"  name_kr={existing.name_kr}, is_current={existing.is_current}")
        sys.exit(0)

    pv = PatchVersion(
        version="12.0.5",
        name_kr="Midnight Season 1",
        season_number=1,
        released_at=date(2026, 4, 21),
        is_current=True,
    )
    session.add(pv)
    session.commit()
    print("INSERT 완료: version=12.0.5")

    # SELECT로 확인
    rows = session.exec(select(PatchVersion)).all()
    print(f"\nSELECT * FROM patch_versions; ({len(rows)}행)")
    for row in rows:
        print(f"  version={row.version!r}  name_kr={row.name_kr!r}  season={row.season_number}  released={row.released_at}  is_current={row.is_current}")
