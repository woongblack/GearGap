# GearGap — Claude Code 가이드

## 프로젝트 한 줄 요약

> "내 캐릭터에 뭐가 빠졌고, 어디서 드롭되나"

WoW 흑마법사(파멸/고통/악마소환) 유저의 파밍 의사결정 피로를 줄이는 도구.
Murlok.io(BiS 착용률) + Wowhead(드롭처) + Blizzard API(캐릭터 장비) 통합.
DPS 시뮬은 스코프 외 — Raidbots 링크로 외부 위임.

---

## 아키텍처

```
Frontend (React + Vite + TS)  →  Vercel
Backend  (FastAPI + Python)   →  GCP Cloud Run (asia-northeast3)
Database (PostgreSQL)         →  Supabase (개발 중: SQLite)
```

## 로컬 실행

```bash
# Frontend
cd frontend && npm install && npm run dev   # localhost:5173

# Backend
cd backend
python -m venv venv && venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload                      # localhost:8000
```

---

## Phase 구조

| Phase | 목표 | 상태 |
|-------|------|------|
| 0 | Blizzard API 검증 + Murlok 파싱 PoC | ✅ 완료 |
| 1 | 장비 갭 대시보드 MVP (슬롯별 갭 + 드롭처 + 착용률) | 진행 중 |
| 2 | 이행 추적 + RAG 학습 모듈 | 예정 |
| 3 | 검증 루프 (개인화 학습, 북극성) | 예정 |

---

## 설계 철학 — 타협 불가 원칙 4가지

1. **투명성 우선** — 모든 숫자에 출처/샘플 크기/갱신 시점 명시. 블랙박스 없음.
2. **도구는 정답을 주지 않는다** — 착용률은 참고자료. 결정은 유저가 한다.
3. **유저 통제권** — 어느 아이템을 파밍할지는 유저가 직접 판단.
4. **한계를 숨기지 않는다** — 데이터 기준(상위 50명, Murlok 기준)을 항상 명시.

**반면교사:** AskMrRobot(AMR) — 블랙박스 추천 → 신뢰 상실. 같은 패턴 절대 금지.

---

## 금지 규칙 (코드/문구 모두)

| 금지 | 대신 |
|------|------|
| "추천", "최적", "정답" | "참고", "후보", "BiS 후보", "착용률 기준" |
| "1위/2위/3위" 순위 | 정렬은 허용, 순위 강조 없음 |
| "AI가 알아서" | 데이터 출처 항상 명시 |
| DPS 시뮬 직접 제공 | Raidbots 링크로 외부 위임 |
| 블랙박스 알고리즘 | 모든 데이터 출처 공개 |

---

## 규칙 파일

- @.claude/rules/design.md — GearGap 철학 / UI 원칙
- @.claude/rules/backend.md — FastAPI / Python 코딩 기준
- @.claude/rules/frontend.md — React / Vite / TypeScript 기준
- @.claude/rules/database.md — PostgreSQL / Supabase / ERD 기준
- @.claude/rules/infrastructure.md — Vercel / Cloud Run / Supabase 인프라
- @.claude/rules/dev-workflow.md — 로컬 개발 흐름
- @.claude/rules/commit.md — 커밋 컨벤션
