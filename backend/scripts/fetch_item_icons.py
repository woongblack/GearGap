"""아이템 아이콘 URL 일괄 fetch → items.icon_url 저장.

Blizzard API media 엔드포인트 사용 (Wowhead tooltip API보다 안정적).

실행:
    cd backend
    python scripts/fetch_item_icons.py

동작:
    - icon_url이 없는 아이템만 대상
    - Blizzard item media API → icon URL 추출 → DB 저장
    - 아이템 간 0.3초 슬립
"""

import sys
import time
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlmodel import Session, select

from app.core.config import settings
from app.core.db import engine
from app.models.item import Item
from app.models.patch import PatchVersion  # noqa: F401 — FK patch_versions 해소용
from app.models.meta import WowClass, Spec  # noqa: F401 — FK 해소용

TOKEN_URL = "https://oauth.battle.net/token"
MEDIA_URL = "https://us.api.blizzard.com/data/wow/media/item/{item_id}"
HEADERS = {"User-Agent": "GearGap/0.1 (contact: woongblack123@gmail.com)"}


def get_token(client: httpx.Client) -> str:
    resp = client.post(
        TOKEN_URL,
        auth=(settings.BLIZZARD_CLIENT_ID, settings.BLIZZARD_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_icon(client: httpx.Client, token: str, item_id: int) -> str | None:
    try:
        resp = client.get(
            MEDIA_URL.format(item_id=item_id),
            params={"namespace": "static-us", "locale": "en_US"},
            headers={**HEADERS, "Authorization": f"Bearer {token}"},
            timeout=10,
        )
        resp.raise_for_status()
        assets = resp.json().get("assets", [])
        icon_url = next((a["value"] for a in assets if a["key"] == "icon"), None)
        return icon_url
    except Exception as e:
        print(f"  [WARN] item {item_id}: {e}")
    return None


def main() -> None:
    with Session(engine) as session:
        items = session.exec(
            select(Item).where(Item.icon_url.is_(None))  # type: ignore[arg-type]
        ).all()

    if not items:
        print("모든 아이템에 icon_url이 이미 있음.")
        return

    print(f"아이콘 없는 아이템 {len(items)}개 처리 시작")

    with httpx.Client(headers=HEADERS) as client:
        token = get_token(client)
        print("Blizzard OAuth 토큰 획득 완료")

        ok_count = 0
        with Session(engine) as session:
            for i, item in enumerate(items, 1):
                url = fetch_icon(client, token, item.id)
                if url:
                    db_item = session.get(Item, item.id)
                    if db_item:
                        db_item.icon_url = url
                        session.add(db_item)
                        session.commit()
                        ok_count += 1
                        print(f"[{i}/{len(items)}] {item.id} {item.name[:30]:<30} → OK")
                else:
                    print(f"[{i}/{len(items)}] {item.id} {item.name[:30]:<30} → 스킵")

                if i < len(items):
                    time.sleep(0.3)

    print(f"\n완료: {ok_count}/{len(items)}개 저장")


if __name__ == "__main__":
    main()
