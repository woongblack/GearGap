# Frontend 코딩 기준 (React 19 + Vite + TypeScript)

## 스택

- React 19 + TypeScript
- Vite 8 (빌드 도구)
- React Router DOM 7
- 스타일: CSS 커스텀 프로퍼티 (CSS 토큰, `styles/tokens.css` 기준)
- 상태관리: useState / localStorage (`useWeights` 훅)

## 실제 디렉토리 구조

```
frontend/src/
├── api/
│   ├── client.ts         # API 호출 함수 (api.getCharacter, api.getEfficiency)
│   └── types.ts          # 백엔드 응답 타입 (ApiCharacter, ApiCandidate 등)
├── screens/              # 라우트 단위 화면 (pages/ 아님)
│   ├── LandingScreen.tsx
│   ├── LoadingScreen.tsx
│   ├── AnalysisScreen.tsx
│   ├── RecommendationsScreen.tsx
│   └── ErrorScreen.tsx
├── components/
│   ├── analysis/         # CharHeader, SlotList, StatBars, StatRadar
│   ├── common/           # ComparisonTable, WeightControls, Prov, MetaDrawer, MetaRibbon
│   ├── search/           # SearchPanel, CharacterCard
│   ├── AppShell.tsx
│   ├── Background.tsx
│   ├── Logo.tsx
│   ├── Toast.tsx
│   └── Topbar.tsx
├── data/
│   ├── mock.ts           # 개발용 목 데이터 (API 연결 전까지 유지)
│   └── types.ts          # 프론트엔드 도메인 타입 (CharProfile, RaidBoss 등)
├── styles/
│   ├── tokens.css        # CSS 커스텀 프로퍼티 (--gold, --bg-deep 등)
│   ├── base.css
│   ├── components.css
│   ├── screens.css
│   └── states.css
├── utils/
│   └── scores.ts         # 효율 점수 정규화 계산
├── App.tsx               # 라우터 + 전역 상태
└── main.tsx
```

## 라우트 구조

```
/                          → LandingScreen
/loading                   → LoadingScreen (state: charName, realm)
/c/:realm/:name            → AnalysisScreen
/c/:realm/:name/recs       → RecommendationsScreen
/errors                    → ErrorScreen
```

## API 클라이언트 사용법

```typescript
import { api } from '../api/client';

// 캐릭터 조회
const character = await api.getCharacter(realm, name);

// 효율 점수 (가중치 파라미터)
const result = await api.getEfficiency(character.id, {
  w_dps: weights.dps,
  w_time: weights.time,
  w_prob: weights.drop,
});
```

## 효율 점수 계산 (frontend)

`utils/scores.ts`에서 정규화 방식으로 계산:
```
nDps  = dpsGain / max(dpsGain)
nTime = 1 - (timeMin / max(timeMin))   ← 시간 짧을수록 유리
nDrop = dropPct / max(dropPct)
score = (nDps×w + nTime×w + nDrop×w) / total   → 0~1
```
백엔드의 절대값 공식과 다름 — API 연결 시 통일 필요.

## 환경 변수

```
VITE_API_URL    # 백엔드 URL (로컬: http://localhost:8000)
```
- `.env.local` 로컬 개발용 (git 추적 안 함)
- Vercel 환경변수에 Production 값 설정

## GearGap UI 원칙

- 효율 점수는 "참고 지표"임을 항상 명시 (CAVEAT 블록 유지)
- 근거 패널 `Prov` 컴포넌트 — 모든 숫자 옆에 배치
- 출처 명시: `dps_sim_profile === "patchwerk"` → `"⚠️ 패치워크 기준"` 표시
- "추천" 대신 "Compare paths", "참고" 언어 사용
- 가중치 슬라이더 변경 → 즉시 재정렬 (debounce 불필요, useMemo로 처리됨)
- 순위 강조("1위" 등) 없음 — 정렬은 허용

## 코드 기준

- 파일/폴더: `kebab-case` (컴포넌트 파일은 `PascalCase.tsx`)
- 컴포넌트/타입: `PascalCase`
- 함수/변수: `camelCase`
- CSS: CSS 커스텀 프로퍼티(`--gold`, `--bg-deep`) 사용, 인라인 스타일은 최소화
- `import type` 사용 (타입 import는 분리)

## 현재 상태 (2026-05-12 기준)

- 전체 화면/컴포넌트 완성, `data/mock.ts` 목 데이터로 동작 중
- `api/client.ts` + `api/types.ts` 추가됨 (백엔드 연결 레이어)
- LandingScreen → LoadingScreen 전환은 setTimeout 기반 (실제 API 호출 미연결)
- AnalysisScreen, RecommendationsScreen → 아직 mock 데이터 사용
