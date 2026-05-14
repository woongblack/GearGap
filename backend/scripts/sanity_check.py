"""선결 준비물 sanity check"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from sqlmodel import Session, select
from app.core.db import engine
from app.models.patch import PatchVersion

# .env 키 존재 확인 (값 출력 X)
rh = os.getenv("RAIDBOTS_HASH")
cpv = os.getenv("CURRENT_PATCH_VERSION")
print("=== .env 키 확인 ===")
print(f"RAIDBOTS_HASH:          {'OK' if rh else 'MISSING'}")
print(f"CURRENT_PATCH_VERSION:  {cpv if cpv else 'MISSING'}")

# patch_versions SELECT
print("\n=== patch_versions ===")
with Session(engine) as session:
    rows = session.exec(select(PatchVersion)).all()
    if not rows:
        print("  (행 없음)")
    for row in rows:
        print(f"  version={row.version!r}  name_kr={row.name_kr!r}  season={row.season_number}  released={row.released_at}  is_current={row.is_current}")

print("\n=== 결과 ===")
ok = rh and cpv and cpv == "12.0.5" and rows and rows[0].version == "12.0.5"
print("PASS" if ok else "FAIL")
