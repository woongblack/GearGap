"""contents.name_kr 일괄 업데이트.

실행:
    cd backend
    python scripts/seed_content_name_kr.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlmodel import Session, text

from app.core.db import engine

NAME_KR_MAP: dict[str, str] = {
    # 레이드
    "The Voidspire":            "공허첨탑",
    "The Dreamrift":            "꿈의 균열",
    "March on Quel'Danas":      "쿠엘다나스 진격로",
    "World Bosses":             "월드 보스",
    # 신규 던전
    "Nexus-Point Xenas":        "공결탑 제나스",
    "Maisara Caverns":          "마이사라 동굴",
    "Windrunner Spire":         "윈드러너 첨탑",
    "Murder Row":               "마법학자의 정원",
    # 레거시 던전
    "Magisters' Terrace":       "마법사의 테라스",
    "Skyreach":                 "하늘탑",
    "Algeth'ar Academy":        "알게타르 대학",
    "Pit of Saron":             "사론의 구덩이",
    "Seat of the Triumvirate":  "삼두정의 권좌",
    "Den of Nalorakk":          "날로라크의 소굴",
    "The Blinding Vale":        "눈부신 골짜기",
}


def main() -> None:
    with Session(engine) as session:
        updated = 0
        for name_en, name_kr in NAME_KR_MAP.items():
            result = session.exec(
                text("UPDATE contents SET name_kr = :name_kr WHERE name_en = :name_en"),
                params={"name_kr": name_kr, "name_en": name_en},
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
            text("SELECT name_en, name_kr, type FROM contents ORDER BY type, name_en")
        ).fetchall()
        print("\n[최종 상태]")
        for r in rows:
            kr = r.name_kr or "(NULL)"
            print(f"  {r.type:<10} {r.name_en:<35} → {kr}")


if __name__ == "__main__":
    main()
