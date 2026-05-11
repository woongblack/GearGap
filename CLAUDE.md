# GearGap — Claude Code 가이드

## 프로젝트 한 줄 요약

> "흩어진 와우 데이터를 합쳐 보여주는 투명한 대시보드. 도구는 정답을 주지 않고, 결정은 유저가 합니다."

WoW 흑마법사(파멸/고통/악마소환) 유저의 파밍 의사결정 피로를 줄이는 도구.
bloodmallet(DPS Gain) + Wowhead(드롭률) + Raider.IO(클리어 시간) + Blizzard API(캐릭터) 통합.

---

## 효율 점수 공식

```
효율 점수 = (dps_gain × W_dps) ÷ (avg_clear_minutes × W_time) × (drop_rate × W_prob)
```

가중치(W_*)는 유저가 슬라이더로 직접 조정 (0.5~2.0). 실시간 재계산.

---

## 아키텍처

```
Frontend (React + Vite + TS)  →  Vercel
Backend  (FastAPI + Python)   →  GCP Cloud Run (asia-northeast3)
Database (PostgreSQL)         →  Supabase (+ pgvector for Phase 2)
```

## 로컬 실행

```bash
# Frontend
cd frontend && npm install && npm run dev   # localhost:5173

# Backend
cd backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload                         # localhost:8000
```

---

## Phase 구조

| Phase | 목표 | 상태 |
|-------|------|------|
| 0 | Walking Skeleton (Blizzard API + 인프라 검증) | 진행 중 |
| 1 | 투명 대시보드 MVP (흑마 캐릭터 dogfooding 가능) | 예정 |
| 2 | 이행 추적 + RAG 학습 모듈 (LangChain + pgvector) | 예정 |
| 3 | 검증 루프 (개인화 학습, 북극성) | 예정 |

---

## 설계 철학 — 타협 불가 원칙 4가지

1. **투명성 우선** — 모든 숫자에 출처/계산식 명시. 블랙박스 없음.
2. **도구는 정답을 주지 않는다** — 효율 점수는 참고자료. 결정은 유저가 한다.
3. **가중치는 유저의 것이다** — DPS/시간/확률 비중을 유저가 조정.
4. **한계를 숨기지 않는다** — 시뮬은 패치워크 기준임을 항상 명시.

**반면교사:** AskMrRobot(AMR) — 블랙박스 추천 → 신뢰 상실. 같은 패턴 절대 금지.

---

## 금지 규칙 (코드/문구 모두)

| 금지 | 대신 |
|------|------|
| "추천", "최적", "정답" | "참고", "후보", "효율 점수" |
| "1위/2위/3위" 순위 | 정렬은 허용, 순위 강조 없음 |
| "AI가 알아서" | 계산 근거 항상 명시 |
| 가중치 하드코딩 | 유저가 슬라이더로 조정 |
| 블랙박스 알고리즘 | 모든 계산식 공개 |

---

## 규칙 파일

- @.claude/rules/design.md — GearGap 철학 / UI 원칙
- @.claude/rules/backend.md — FastAPI / Python 코딩 기준
- @.claude/rules/frontend.md — React / Vite / TypeScript 기준
- @.claude/rules/database.md — PostgreSQL / Supabase / ERD 기준
- @.claude/rules/infrastructure.md — Vercel / Cloud Run / Supabase 인프라
- @.claude/rules/dev-workflow.md — 로컬 개발 흐름
- @.claude/rules/commit.md — 커밋 컨벤션
