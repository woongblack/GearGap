# GearGap

> **"내 캐릭터에 뭐가 빠졌고, 어디서 드롭되나"**
>
> WoW 흑마법사 유저의 파밍 의사결정 피로를 줄이는 투명한 장비 갭 대시보드.

---

## 🎯 무엇을 하는 도구인가

상위 플레이어들이 실제로 착용하는 아이템과 내 캐릭터 장비를 비교해 **갭을 시각화**하고, 각 아이템의 **드롭처(레이드 보스 / 던전)**를 함께 제공한다.

DPS 시뮬레이션은 GearGap의 역할이 아니다. 시뮬이 필요한 유저는 Raidbots로 연결한다.

---

## 📐 설계 철학 (타협 불가)

1. **투명성 우선** — 모든 숫자에 출처 / 샘플 크기 / 갱신 시점 명시. 블랙박스 없음.
2. **도구는 정답을 주지 않는다** — 착용률은 참고자료. 결정은 유저가 한다.
3. **유저 통제권** — 어느 아이템을 파밍할지는 유저가 직접 판단.
4. **한계를 숨기지 않는다** — 데이터 기준(상위 50명, Murlok 기준)을 항상 명시.

**반면교사:** AskMrRobot(AMR) — 블랙박스 추천 → 신뢰 상실.

---

## 🔍 데이터 소스

| 데이터 | 소스 | 갱신 주기 |
|---|---|---|
| 캐릭터 현재 장비 | Blizzard Battle.net API | 실시간 (10분 캐시) |
| 스펙별 BiS 착용률 (상위 50명) | Murlok.io 크롤링 | 1일 1회 |
| 아이템 드롭처 | Wowhead tooltip API | 패치 단위 |
| 인스턴스 / 시즌 메타 | Raidbots static JSON | 패치 단위 |

---

## 🏗️ 아키텍처

```
Frontend (React + Vite + TS)  →  Vercel
Backend  (FastAPI + Python)   →  GCP Cloud Run (asia-northeast3)
Database (PostgreSQL)         →  Supabase (개발 중: SQLite)
```

---

## 🚀 로컬 실행

```bash
# Frontend (localhost:5173)
cd frontend
npm install
npm run dev

# Backend (localhost:8000)
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🗺️ Phase 구조

| Phase | 목표 | 상태 |
|---|---|---|
| 0 | Blizzard API 검증 + Murlok 파싱 PoC | ✅ 완료 |
| 1 | 장비 갭 대시보드 MVP — 슬롯별 갭 + 드롭처 + 착용률 | 🔄 진행 중 |
| 2 | 이행 추적 + RAG 학습 모듈 | 예정 |
| 3 | 검증 루프 — 개인화 학습 (북극성) | 예정 |

---

## 🚫 하지 않을 것

- ❌ DPS 시뮬 직접 제공 (Raidbots 링크로 위임)
- ❌ "1위/2위/3위" 순위 강조
- ❌ "이거 가세요" 명령형 추천
- ❌ 블랙박스 알고리즘 (모든 데이터 출처 공개)

---

## 📦 레포 구조

```
GearGap/
├── frontend/      # React + Vite + TypeScript
├── backend/       # FastAPI + Python
│   ├── app/
│   │   ├── models/       # SQLModel DB 스키마
│   │   ├── services/     # blizzard.py, murlok.py
│   │   └── api/v1/       # REST 엔드포인트
│   ├── alembic/          # DB 마이그레이션
│   └── scripts/          # PoC + 검증 스크립트
├── docs/          # 작업 지시서 / 브리핑 문서
└── CLAUDE.md      # Claude Code 가이드
```

---

## 📬 Contact

**정재웅** · [github.com/woongblack](https://github.com/woongblack) · woongblack123@gmail.com

*마지막 업데이트: 2026-05-13 (v0.6)*
