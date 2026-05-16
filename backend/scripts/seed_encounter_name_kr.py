"""encounters.name_kr 일괄 업데이트 (레이드 넴드).

실행:
    cd backend
    python scripts/seed_encounter_name_kr.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlmodel import Session, text

from app.core.db import engine

NAME_KR_MAP: dict[str, str] = {
    # The Voidspire (공허첨탑)
    "Imperator Averzian":          "전제군주 아베르지안",
    "Vorasius":                    "보라시우스",
    "Fallen-King Salhadaar":       "몰락한 왕 살라다르",
    "Vaelgor & Ezzorak":           "바엘고어와 에조라크",
    "Lightblinded Vanguard":       "빛에 눈이 먼 선봉대",
    "Crown of the Cosmos":         "우주의 왕관",
    # The Dreamrift (꿈의 균열)
    "Chimaerus the Undreamt God":  "꿈결을 벗어난 신 카이메루스",
    # March on Quel'Danas (쿠엘다나스 진격로)
    "Belo'ren, Child of Al'ar":    "알라르의 자손 벨로렌",
    "Midnight Falls":              "한밤의 도래",
}


def main() -> None:
    with Session(engine) as session:
        updated = 0
        for name_en, name_kr in NAME_KR_MAP.items():
            result = session.exec(
                text("UPDATE encounters SET name_kr = :name_kr WHERE name = :name"),
                params={"name_kr": name_kr, "name": name_en},
            )
            rows = result.rowcount
            if rows:
                print(f"  OK  {name_en:<35} → {name_kr}")
                updated += rows
            else:
                print(f"  --  {name_en:<35} (해당 행 없음)")

        session.commit()

    print(f"\n완료: {updated}개 업데이트")

    # 결과 확인
    with Session(engine) as session:
        rows = session.exec(
            text("""
                SELECT e.name, e.name_kr, c.name_en AS instance
                FROM encounters e
                JOIN contents c ON e.content_id = c.id
                WHERE e.name_kr IS NOT NULL
                ORDER BY c.name_en, e.name
            """)
        ).fetchall()
        print("\n[name_kr 설정된 넴드]")
        for r in rows:
            print(f"  [{r.instance}] {r.name} → {r.name_kr}")


if __name__ == "__main__":
    main()
