# GearGap

> **WoW 의사결정 피로 완화를 위한 투명 대시보드**
>
> 흩어진 데이터(SimC 시뮬, Wowhead 드롭, Blizzard 캐릭터 정보)를 합쳐 보여주고,
> 유저가 스스로 파밍 로드맵을 결정할 수 있도록 돕는 도구.

---

## 🌟 북극성 (North Star)

> "유저가 GearGap의 정보를 보고 스스로 결정한 로드맵을, 실제로 이행했을 때 그 결과가 본인에게 맞아 들어가는 경험"

**신뢰는 알고리즘의 명성에서 오지 않는다. 본인의 이행 결과로 쌓인다.**

---

## 🎯 시작점 — 진짜 문제

```
"뭘 먹어야 할지는 알아.
 Archon, Wowhead, bloodmallet 다 보면 나와있어.
 근데 그 수가 너무 많고, 내 시간은 제한적이야.

 어디부터 가야 가장 스펙업에 도움이 되지?"
```

이건 **추천 문제가 아니라 정보 통합/우선순위 시각화 문제**다.

---

## 📐 설계 철학

이 4가지는 타협 불가능한 원칙이다.

### 1. 투명성 우선 (Transparency First)
모든 숫자에는 출처와 계산식이 따라온다. 블랙박스 없음.

### 2. 도구는 정답을 주지 않는다
효율 점수는 추천이 아니라 **참고자료**다. 결정은 유저가 한다.

### 3. 가중치는 유저의 것이다
DPS / 시간 / 확률의 비중을 유저가 조정할 수 있다.

### 4. 한계를 숨기지 않는다
시뮬은 패치워크 기준임을 항상 명시한다. **실전 ≠ 시뮬.**

---

## 🚫 하지 않을 것 (Anti-Patterns)

AskMrRobot 실패 사례에서 도출한 금지 사항.

- ❌ 자체 시뮬 엔진 개발 (SimC가 이미 신뢰받음)
- ❌ "1위/2위/3위" 같은 순위 강조 표시
- ❌ "이거 가세요" 같은 명령형 문구
- ❌ 가중치 하드코딩 (유저가 조정 가능해야 함)
- ❌ 데이터 출처 숨기기 (모든 숫자에 출처 따라가야 함)
- ❌ 시뮬 한계를 숨기기 (패치워크 기준임을 항상 명시)

---

## 🔍 차별점

| 도구 | 영역 | 한계 |
|---|---|---|
| Archon | 메타/티어 빌드 | 내 캐릭터 무관 |
| bloodmallet | 시뮬 시각화 (DPS Gain) | 일반 프로필 기준 |
| Raidbots | 시뮬 (내 캐릭터 입력) | "결과"만 제공, 우선순위 없음 |
| AskMrRobot ❌ | "Best in Bags" 자동 추천 | **블랙박스 → 신뢰 상실** |
| **GearGap** | **위 데이터들의 통합 + 시간 효율 시각화 + 유저 가중치 조정** | — |

GearGap은 **새로운 시뮬 엔진을 만들지 않는다.**
이미 신뢰받는 도구들의 데이터를 **합쳐서 보여주고, 유저가 스스로 판단할 수 있도록 돕는다.**

---

## 🧮 핵심 도메인 개념

### 효율 점수 (Efficiency Score)

```
Efficiency = (DPS Gain × W_dps) ÷ (Time Cost × W_time) × (Drop Probability × W_prob)
```

| 요소 | 정의 | 데이터 소스 | 한계 명시 |
|---|---|---|---|
| DPS Gain | 아이템 장착 시 예상 DPS 향상량 | bloodmallet (SimC) | 패치워크 기준 |
| Time Cost | 콘텐츠 1회 클리어 평균 소요 시간 | Raider.IO | 공대 수준에 따라 다름 |
| Drop Probability | 아이템 드롭 확률 | Wowhead | 통계적 평균 |
| W_dps, W_time, W_prob | **유저 가중치** | 슬라이더 조정 | 기본값 1.0 |

> ⚠️ **이 점수는 순위가 아니라 참고 지표다.** UI에서 "1위/2위" 같은 표기는 금지한다.

### 검증 루프 (Verification Loop) — 북극성 기능

GearGap의 진짜 차별점이자 장기 비전.

```
T0: 로드맵 제시 (현재 DPS 스냅샷 + 후보 콘텐츠)
        ↓
유저가 결정 (어디 갈지)
        ↓
T0 + 7일: 다시 캐릭터 조회
   - 무엇을 먹었나? (Blizzard API)
   - 시뮬 예측 vs 실측 DPS (Warcraft Logs)
        ↓
갭 분석 → 다음 로드맵 보정
   "이 유저는 시뮬 대비 실전 80%"
   "이동 많은 보스 가중치 ↓"
   "본인 자주 가는 던전 가중치 ↑"
```

이 루프가 GearGap의 신뢰를 만든다.

- AMR: "우리 알고리즘 믿으세요" → 신뢰 상실
- GearGap: "당신 데이터로 당신에게 맞춰가요" → 신뢰 자가 생성

> ⚠️ Phase 1에서는 구현하지 않음. 모든 설계 결정의 방향성으로만 사용.

---

## 🛠️ 기술 스택

| 레이어 | 기술 | 선택 이유 |
|---|---|---|
| Backend | Python / FastAPI | 데이터 수집/가공 생태계, AI 연동 친화적 |
| Database | MySQL | 아이템/드롭/스냅샷 데이터 정형화 |
| AI (Phase 2+) | Anthropic Claude API | 추천 근거 자연어 생성 |
| Frontend | React | 심플한 결과 UI |
| 외부 API | Blizzard API, bloodmallet, Wowhead, Warcraft Logs | 캐릭터/시뮬/드롭/실측 데이터 |

---

## 🚀 실행 방법

### Repository 구조

```
GearGap/
├── frontend/       # React + Vite + TypeScript (UI and logic)
├── backend/        # FastAPI Python backend (Data fetching and processing)
├── .gitignore
└── README.md
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

프론트엔드: `http://localhost:5173`

### Backend

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

백엔드 API: `http://localhost:8000`

---

## 📦 스코프 (MVP)

### 콘텐츠 범위
- **레이드**: 한밤의 요새 (넴드 8개) — 일반 / 영웅 / 신화
- **쐐기 (미식)**: TWW 시즌 2 던전 풀 (8개)

### 지원 직업/스펙
- MVP: **흑마법사 3개 스펙** (파멸 / 고통 / 악마소환)

---

## 🗺️ 개발 로드맵

### Phase 0 — 데이터 소스 검증
- [ ] bloodmallet 데이터 접근성 확인
- [ ] bloodmallet 라이선스/이용 약관 검토
- [ ] Blizzard API Client ID 발급
- [ ] Wowhead 드롭 데이터 수집 가능성 확인

### Phase 1 (MVP) — 투명 대시보드
- [ ] Blizzard API 연동 + 캐릭터 장비 수집
- [ ] bloodmallet 데이터 수집 파이프라인
- [ ] 한밤 + 시즌2 드롭 테이블 구축
- [ ] 효율 점수 계산 엔진 (가중치 조정 가능)
- [ ] FastAPI REST API
- [ ] React UI: 검색 / 통합 시각화 / 가중치 조정 / 근거 패널

### Phase 2 — 이행 추적
- [ ] 캐릭터 스냅샷 저장/조회
- [ ] 변화 감지 (이전 vs 현재)
- [ ] Warcraft Logs API 연동
- [ ] 시뮬 예측 vs 실측 비교 UI
- [ ] Claude API로 변화 자연어 설명

### Phase 3 — 검증 루프 (북극성 ⭐)
- [ ] 개인 보정치 학습 알고리즘
- [ ] 유저별 신뢰도 지표
- [ ] 컨텍스트 인식 가중치 자동 조정 (투명하게 명시)
- [ ] 다른 직업/스펙 확장

---

## 📊 시스템 흐름 (Phase 1)

```
[유저] 캐릭터명 + 서버 입력
    ↓
[Blizzard API] 현재 장비 + 스텟 수집
    ↓
[스펙 감지] 파멸 / 고통 / 악마소환
    ↓
[데이터 통합] bloodmallet + Wowhead + Raider.IO
    ↓
[효율 엔진] 가중치 적용 효율 점수 산출
    ↓
[투명 시각화] 모든 숫자 + 출처 + 한계 표시
    ↓
[유저 조정] 가중치 슬라이더로 재계산
    ↓
[유저가 결정] (도구는 결정하지 않음)
```

---

## ❓ 미결 사항 (Open Questions)

| # | 질문 | 우선순위 |
|---|---|---|
| 1 | bloodmallet 데이터 접근 안정성 | **높음** |
| 2 | bloodmallet 이용 약관 / 라이선스 | **높음** |
| 3 | Wowhead vs Blizzard API 드롭 데이터 정확도 | 중간 |
| 4 | 콘텐츠 클리어 시간 데이터 소스 | 중간 |
| 5 | 같은 슬롯 후보 다수 시 처리 방법 | 중간 |
| 6 | 근거 패널 정보 밀도 vs UI 복잡도 | 중간 |

---

## 🪞 Mirror Agent 셀프 검토 변천 기록

본 PRD는 [Mirror Agent](https://github.com/woongblack/mirror-agent) 패턴으로 **세 차례** 자체 검토를 거쳤다.

### v0.1 → v0.2
1. ❌ 다른 카테고리(RAGON)를 비교 대상으로 잡음 → **같은 카테고리(Archon/Raidbots/bloodmallet)로 재설정**
2. ❌ "스텟 갭 = 우선순위" 단순 가정 → **DPS Gain 기반 효율 점수로 전환**
3. ❌ "포트폴리오 멋있어 보이려고" 자체 시뮬 워커 추가 위험 → **bloodmallet 데이터 활용으로 단순화**
4. ❌ Java/Next.js 관성적 선택 → **Python/FastAPI + React**

### v0.2 → v0.3 (시장 검증 후)
5. ❌ "정답 추천 도구" 포지셔닝 — **AMR 실패 사례와 동일한 함정** → **투명 대시보드로 전환**
6. ❌ 블랙박스 알고리즘 가정 → **가중치 조정 가능, 모든 숫자 출처 명시**
7. ❌ 시뮬 데이터 맹신 → **한계 항상 명시 ("패치워크 기준")**
8. ❌ "효율 1위" 강조 → **순위 표기 금지, 참고 지표로 격하**

### v0.3에서 추가된 비전
9. ✅ **검증 루프 도입** — "이행 후 결과 검증"이 진짜 신뢰의 원천
10. ✅ Phase 단계 명확 분리 — Phase 3는 비전이지 MVP 약속이 아님

---

## 💭 마무리

GearGap은 시장 진출이 아닌, **개발자 이전부터 본인이 와우 플레이어로서 풀고 싶었던 문제**를 개발로 푸는 프로젝트다.

세 번의 자체 검토를 거치며 정체성이 명확해졌다:

- ❌ 정답 자판기 (AMR 실패 패턴)
- ✅ **투명 의사결정 대시보드**
- ✅ **장기적으로 본인 이행 데이터로 신뢰가 자라는 도구**

> Loading King이 "기사가 직접 결정한 순서대로 짐을 적재하는 시스템"이었듯,
> GearGap은 **"유저가 직접 결정한 로드맵을 검증해가는 시스템"** 이다.

도구는 정답을 주지 않는다. 정보를 투명하게 정리해서, 유저가 스스로 결정하고, 그 결정의 결과로 신뢰가 쌓이는 구조 — 이것이 GearGap이 AMR과 다를 수 있는 유일한 길이다.

**문제 정의가 먼저, 기술은 그 다음.**

---

## 🔗 관련 프로젝트

- [Loading King](https://github.com/LoadingKingProject/loading_king) — 적재 순서 최적화. "사람의 판단을 구조화한다" 철학의 시작점.
- [Mirror Agent](https://github.com/woongblack/mirror-agent) — 자기 비판 에이전트. GearGap PRD는 Mirror Agent로 세 차례 검토되었음.

---

## 📬 Contact

**정재웅**
- 📧 woongblack123@gmail.com
- 👨‍💻 [github.com/woongblack](https://github.com/woongblack)

---

*마지막 업데이트: 2026-05-02 (PRD v0.3 기준)*
