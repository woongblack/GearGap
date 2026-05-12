# Frontend 코딩 기준 (React 19 + Vite + TypeScript)

## 스택

- React 19 + TypeScript
- Vite 8 (빌드 도구)
- React Router DOM 7
- 스타일: CSS 커스텀 프로퍼티 (CSS 토큰, `styles/tokens.css` 기준)
- 상태관리: useState / localStorage

## 실제 디렉토리 구조

```
frontend/src/
├── api/
│   ├── client.ts         # API 호출 함수 (api.getCharacter, api.getBiS 등)
│   └── types.ts          # 백엔드 응답 타입 (ApiCharacter, ApiBiSCandidate 등)
├── screens/              # 라우트 단위 화면 (pages/ 아님)
│   ├── LandingScreen.tsx
│   ├── LoadingScreen.tsx
│   ├── AnalysisScreen.tsx
│   ├── RecommendationsScreen.tsx
│   └── ErrorScreen.tsx
├── components/
│   ├── analysis/         # CharHeader, SlotList, StatBars, StatRadar
│   ├── common/           # ComparisonTable, Prov, MetaDrawer, MetaRibbon
│   ├── search/           # SearchPanel, CharacterCard
│   ├── AppShell.tsx
│   ├── Background.tsx
│   ├── Logo.tsx
│   ├── Toast.tsx
│   └── Topbar.tsx
├── data/
│   ├── mock.ts           # 개발용 목 데이터 (API 연결 전까지 유지)
│   └── types.ts          # 프론트엔드 도메인 타입 (CharProfile, BiSCandidate 등)
├── styles/
│   ├── tokens.css        # CSS 커스텀 프로퍼티 (--gold, --bg-deep 등)
│   ├── base.css
│   ├── components.css
│   ├── screens.css
│   └── states.css
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

// BiS 후보 조회 (슬롯별 착용률)
const bis = await api.getBiS(character.class_name, character.spec_name);
```

## 환경 변수

```
VITE_API_URL    # 백엔드 URL (로컬: http://localhost:8000)
```
- `.env.local` 로컬 개발용 (git 추적 안 함)
- Vercel 환경변수에 Production 값 설정

## GearGap UI 원칙

- 착용률 데이터 출처 항상 표시 (`Murlok.io 기준, 상위 50명`)
- 갱신 시점 표시 (`scraped_at` 기준)
- "추천" 대신 "BiS 후보", "참고" 언어 사용
- 순위 강조("1위" 등) 없음 — 정렬은 허용
- DPS 시뮬 필요 시 Raidbots 링크로 외부 연결 (GearGap 스코프 외)

## 코드 기준

- 파일/폴더: `kebab-case` (컴포넌트 파일은 `PascalCase.tsx`)
- 컴포넌트/타입: `PascalCase`
- 함수/변수: `camelCase`
- CSS: CSS 커스텀 프로퍼티(`--gold`, `--bg-deep`) 사용, 인라인 스타일은 최소화
- `import type` 사용 (타입 import는 분리)
