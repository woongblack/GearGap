# Handoff: GearGap — WoW Item Recommendation Service

## Overview
GearGap is a World of Warcraft 장비 추천 웹 서비스. 캐릭터명 + 서버를 입력하면 현재 템셋을 분석하고, 상위 1% 유저 데이터를 기반으로 스텟 갭을 계산해 "어느 레이드 몇 넴드" 또는 "어느 쐐기 던전 몇 키"에서 어떤 아이템을 드세요라고 추천한다.

타겟 유저는 20-30대 WoW 플레이어이며, 비주얼 톤은 다크 + 골드 액센트의 게이밍 UI다 (Raider.IO, RAGON 같은 분석 사이트의 결).

## About the Design Files
이 폴더의 HTML/JSX 파일은 **디자인 레퍼런스**입니다 — 의도한 외관과 동작을 보여주는 프로토타입이지, 그대로 운영에 올릴 코드가 아닙니다. 이 핸드오프의 작업은 **타겟 코드베이스(요청대로 Vite + React + TypeScript + React Router + 일반 CSS)에서 이 디자인을 재구성하는 것**입니다.

## Target Stack
- **Vite** (build/dev)
- **React 18** (UI)
- **TypeScript** (strict)
- **React Router v6** (routing)
- **CSS 그대로 유지** — 기존 `screens.css` 와 인라인 스타일 변수를 컴포넌트 단위로 분할 (CSS Modules 권장)
- 아이콘은 인라인 SVG (외부 의존성 없음)
- 데이터 레이어는 mock 모듈 (`src/data/`) 로 시작 — 추후 API 교체 자리만 typed interface 로 정의

## Fidelity
**High-fidelity.** 색상, 타이포그래피, 스페이싱, 모션, 호버/포커스 상태가 모두 최종 의도된 값입니다. 픽셀 단위로 재현해주세요.

---

## Routes

| Path | Component | Purpose |
| --- | --- | --- |
| `/` | `LandingScreen` | 캐릭터 검색, 최근 검색 카드 |
| `/c/:realm/:name` | `AnalysisScreen` | 스텟 갭, 슬롯 갭 시각화 |
| `/c/:realm/:name/recs` | `RecommendationsScreen` | 레이드/쐐기 탭 추천 리스트 |

레이아웃은 모두 공통 `<AppShell>` 안에서 렌더링 (Topbar + footer + 백그라운드 atmospheric layers + ScreenSwitcher 핀 + Tweaks 패널은 제거 가능).

---

## Design Tokens

CSS variables on `:root` (use them — do not hardcode the hex):

```css
--bg-deep:     oklch(0.16 0.012 60);   /* outer background */
--bg:          oklch(0.19 0.012 60);   /* base background */
--panel:       oklch(0.225 0.014 65);  /* cards/panels */
--panel-2:     oklch(0.26 0.015 65);   /* card gradient stop */
--border:      oklch(0.34 0.014 65);   /* primary border */
--border-soft: oklch(0.28 0.012 65);   /* divider */
--text:        oklch(0.94 0.012 80);   /* primary text */
--text-dim:    oklch(0.72 0.014 75);   /* secondary text */
--text-mute:   oklch(0.55 0.012 70);   /* tertiary/labels */
--gold:        oklch(0.80 0.135 78);   /* primary accent */
--gold-deep:   oklch(0.66 0.13 65);    /* accent dark / borders */
--crimson:     oklch(0.62 0.16 25);    /* high-gap warning */
--jade:        oklch(0.66 0.10 160);   /* healer / positive */
--steel:       oklch(0.66 0.08 230);   /* dps-arcane / mid priority */
--violet:      oklch(0.66 0.13 300);   /* tank / warlock */
```

**Typography**
- Display/headline: `'Cinzel', serif` (Google Fonts, weights 500/600/700)
- UI/body: `'Inter', system-ui, sans-serif` (weights 400/500/600/700)
- Labels/mono: `'JetBrains Mono', monospace` (weights 400/500)

**Spacing**: 4 / 8 / 12 / 14 / 16 / 18 / 22 / 24 / 28 / 32 / 48 / 64 / 80 / 96 px scale.
**Radius**: 2, 3, 4 px (작게 유지 — 다크 게이밍 톤). `999px` for pills/dots only.
**Shadow**: `0 30px 60px -20px oklch(0 0 0 / 0.5)` (panels), `0 0 8px var(--gold)` (glow dots).

---

## Atmospheric Layers (전역 배경)

`<body>` 위에 4겹의 `position: fixed; inset: 0; pointer-events: none;` 레이어:
1. **bg-vignette** — radial gradient (위쪽 골드 톤 + 아래쪽 다크)
2. **bg-grid** — 64px x 64px 그리드 라인, 중앙으로 `mask-image` radial fade
3. **bg-sigil** — 중앙 정렬 SVG (이중 원 + 별표 두 개), 6% opacity
4. **bg-grain** — fractal noise SVG (overlay blend, 8% opacity)

→ 자세한 SVG/CSS는 원본 `GearGap.html` `<style>` 블록 참조.

---

## Component Inventory

### 1. `<Topbar>`
- 22px 상하 패딩, 하단 `1px solid var(--border-soft)`
- 좌측: `<Logo>` (32x32 SVG mark + "Gear" + 골드 "Gap")
- 우측: 텍스트 링크 5개 (Search / Analysis / Recommendations / Leaderboards / Sign In 버튼)
- 링크: 13px, `text-mute` → hover/active 시 gold

### 2. `<SearchPanel>` (Landing hero)
- max-width 720px, 1px gold-deep 외곽선 + 4코너 `::before / ::after` 데코
- 3-column grid: `1fr 220px auto`
- 각 필드: 라벨(JetBrains Mono 10px uppercase) + input/select
- 포커스 시 라벨 색을 gold로 + 미세 골드 배경
- 우측 Analyze 버튼: 골드 그라디언트 + Cinzel 폰트 + 검색 아이콘

### 3. `<CharacterCard>` (Recent grid 4-col)
- panel 배경, 좌측 2px 역할 컬러 strip (`::before`)
- 우측 상단 absolute "+8 ilvl" gap badge
- 44px 정사각 portrait (이니셜 글자 + 역할 컬러 그라디언트 오버레이)
- 캐릭터명 (Cinzel) + 스펙 (역할 색)
- 하단: ilvl (Cinzel 20px gold) | 서버 + timestamp
- Hover: lift 2px + 골드 glow

### 4. `<CharHeader>` (Analysis/Recs 상단)
3-col grid: 96px portrait | meta | 우측 percentile
- portrait: 4코너 골드 `::before` 데코
- meta: 이름 (Cinzel 32px) + 태그 칩 4개 + ilvl/score/class row
- percentile: 56px Cinzel "TOP 18%" + sub label + "상위 1%까지 17 ilvl"

### 5. `<StatRadar>` (SVG)
- 360x360 viewBox, center 180,180, radius 130
- 4개 스텟 축 (HASTE / CRIT / MAST / VERS)
- ring polygons at 0.25/0.5/0.75/1.0
- 타겟 polygon: gold dashed `stroke-dasharray: 3 4`, fill `oklch(0.66 0.13 65 / 0.08)`
- 현재 polygon: violet, fill `oklch(0.66 0.13 300 / 0.18)`
- 각 vertex에 violet 점 (3.5px radius, dark stroke)
- 외부 axis 라벨 (mono 10px)
- 정규화: 표시 max = `target * 1.15` 이므로 타겟이 ~0.87 위치

### 6. `<StatBars>`
- 행: `60px 1fr auto` grid
- 트랙 6px (bg-deep + border-soft), violet 그라디언트 fill, gold 2px target marker
- gap >= 5 면 fill을 crimson 그라디언트로, gap 텍스트도 crimson

### 7. `<SlotList>`
- 16개 슬롯 (head, neck, shoulder, cloak, chest, wrist, hands, waist, legs, feet, ring1, ring2, trinket1, trinket2, mainhand, offhand)
- 행: `32px 96px 1fr auto auto` grid
- `hot` 슬롯 (gap >= 10): 좌측 2px gold border + 골드 배경 + 아이콘 골드 보더
- gap pill: `+13` 우측 정렬, 4px-mini bar (crimson glow 시 high)
- 갭 클래스: `zero` (jade) / `med` (gold) / `high` (crimson)

### 8. `<CTABar>`
- 좌측 글로우 그라디언트 + 4코너 `::before / ::after` 데코
- 좌측: title (Cinzel 18px) + sub
- 우측: 골드 그라디언트 버튼 + 화살표 아이콘
- 마진 `28px 0 80px`

### 9. `<Tabs>` (Recs)
- flex, 하단 `1px solid border-soft`
- 탭: 14/22 패딩, Cinzel 600, active 시 gold + `border-bottom 2px gold`
- 각 탭에 count pill (mono 11px, 999px radius)

### 10. `<BossCard>` / `<DungeonCard>`
- panel 배경, padding 16/20
- `priority === 'high'` (또는 dungeon `score >= 70`): 골드 보더 + 좌측 3px glow strip (`::before`)
- `boss-top`: `38px 1fr auto` — 보스 번호(Cinzel 24px) | 이름 한/영 | priority + difficulty 뱃지
- `boss-item` 타일: 40px 아이콘 + 아이템명(gold 14px) + 슬롯/소스 mono + ilvl(Cinzel 22px)
- `boss-why` 인용 박스: bg-deep alpha + 좌측 2px gold-deep + AI 9px 라벨 + 본문 + 우측 stat gain
- DungeonCard 추가: `dgn-score` 진행 바 (label + track + 점수)
- 호버: `<ItemTooltip>` 표시

### 11. `<ItemTooltip>` (호버 시)
- 280px 폭, absolute, top: 100% + 8px margin
- 골드-deep 1px border, dark BG (98% alpha)
- name (gold 14px) + meta (mono 10px) + stamina/intellect (text-violet) + divider + 보조 스텟 + flavor text (italic)
- 호버 시 `opacity 0 → 1`, `translateY -4 → 0` (150ms)

### 12. `<GapSidebar>` (Recs 우측 sticky)
- 320px 폭, `position: sticky; top: 24px`
- panel head + 2x2 summary grid + 4 stat bars + foot (sync time + LIVE pulse dot)
- 스텟 바: 4px height violet, 1px gold target marker

### 13. `<Toast>`
- 검색 시 상단 중앙 표시
- panel BG + gold-deep border, 12x20 padding
- 좌측 12px 골드 spinner (border + animation)
- 진입: `translateY -20 → 0`, opacity 0 → 1 (250ms)

---

## Data Models (TypeScript)

```ts
// src/data/types.ts

export type ClassRole = 'tank' | 'healer' | 'dps-arcane' | 'dps-warlock' | 'dps-melee';

export interface Realm {
  value: string;
  label: string; // Korean realm name
  region: 'KR';
}

export interface RecentChar {
  name: string;
  initial: string;
  spec: string;
  role: ClassRole;
  ilvl: number;
  realm: string;
  when: string;
  gap: string;
  gapColor: 'gold' | 'jade' | 'crimson';
}

export interface CharProfile {
  name: string;
  realm: string;
  region: 'KR';
  classSpec: string;
  classKo: string;
  specKo: string;
  classRole: ClassRole;
  ilvl: number;
  percentile: number;
  score: number;
  level: number;
  avatarInitial: string;
  lastUpdated: string;
}

export interface StatGap {
  key: 'haste' | 'crit' | 'mastery' | 'versatility';
  label: string;
  short: 'HASTE' | 'CRIT' | 'MAST' | 'VERS';
  current: number;
  target: number;
  unit: '%';
  priority: number;
}

export interface SlotItem {
  slot: 'head' | 'neck' | 'shoulder' | 'cloak' | 'chest' | 'wrist' | 'hands'
      | 'waist' | 'legs' | 'feet' | 'ring1' | 'ring2'
      | 'trinket1' | 'trinket2' | 'mainhand' | 'offhand';
  ko: string;
  name: string;
  ilvl: number;
  gap: number;
  source: string;
  hot?: boolean;
}

export type Difficulty = 'normal' | 'heroic' | 'mythic';
export type Priority = 'high' | 'med' | 'low';

export interface RaidBoss {
  idx: number;
  name: string;
  nameEn: string;
  item: string;
  slot: string;       // localized
  slotKey: SlotItem['slot'];
  ilvl: number;
  difficulty: Difficulty;
  priority: Priority;
  why: string;        // AI reason
  gain: string;       // "+8.4"
  stat: string;       // "특화"
}

export interface Dungeon {
  idx: number;
  name: string;
  nameEn: string;
  item: string;
  slot: string;
  slotKey: SlotItem['slot'];
  ilvl: number;
  key: string;        // "M+11"
  drop: string;       // "4번째 보스"
  why: string;
  score: number;      // 0-100 efficiency
  gain: string;
  stat: string;
}
```

Mock data lives in `src/data/mock.ts` — see the included `data.js` for shape and values.

---

## Folder Structure

```
geargap/
├─ index.html
├─ package.json
├─ tsconfig.json
├─ vite.config.ts
├─ public/
│   └─ fonts.css
└─ src/
    ├─ main.tsx
    ├─ App.tsx
    ├─ routes.tsx
    ├─ styles/
    │   ├─ tokens.css       // :root variables
    │   ├─ base.css         // body, atmospherics, .shell
    │   ├─ components.css   // .topbar, .search-panel, .char-card, ...
    │   └─ screens.css      // analysis + recs (포팅 그대로 OK)
    ├─ components/
    │   ├─ AppShell.tsx
    │   ├─ Topbar.tsx
    │   ├─ Logo.tsx
    │   ├─ Toast.tsx
    │   ├─ Background.tsx       // vignette + grid + sigil + grain
    │   ├─ search/
    │   │   ├─ SearchPanel.tsx
    │   │   └─ CharacterCard.tsx
    │   ├─ analysis/
    │   │   ├─ CharHeader.tsx
    │   │   ├─ StatRadar.tsx
    │   │   ├─ StatBars.tsx
    │   │   └─ SlotList.tsx
    │   └─ recs/
    │       ├─ Tabs.tsx
    │       ├─ BossCard.tsx
    │       ├─ DungeonCard.tsx
    │       ├─ ItemTooltip.tsx
    │       ├─ GapSidebar.tsx
    │       └─ CTABar.tsx
    ├─ screens/
    │   ├─ LandingScreen.tsx
    │   ├─ AnalysisScreen.tsx
    │   └─ RecommendationsScreen.tsx
    └─ data/
        ├─ types.ts
        ├─ mock.ts          // RECENT, CHAR, STATS, SLOTS, RAID, DUNGEONS
        ├─ realms.ts
        └─ api.ts           // (placeholder) fetchProfile / fetchRecs
```

---

## Routing

```tsx
// src/routes.tsx
<Routes>
  <Route element={<AppShell />}>
    <Route path="/" element={<LandingScreen />} />
    <Route path="/c/:realm/:name" element={<AnalysisScreen />} />
    <Route path="/c/:realm/:name/recs" element={<RecommendationsScreen />} />
  </Route>
</Routes>
```

- 검색 폼 제출 → `navigate(`/c/${realm}/${name}`)`
- "추천 보기" CTA → `navigate(`/c/${realm}/${name}/recs`)`
- 빵부스러기는 `<Link>` 사용

---

## Interactions / Behavior

- **Search submit**: 빈 값이면 무시. 1.4s 토스트 표시 후 분석 화면으로 라우팅 (실제 API 연결 시 토스트는 spinner 유지 / 에러 시 빨간 toast).
- **Recent card click**: 분석 화면으로 라우팅.
- **Analyze CTA**: 추천 화면으로 라우팅.
- **Tabs**: Raid ↔ Mythic+ 즉시 전환 (URL search param `?tab=raid|mplus` 권장).
- **Item tooltip**: CSS 호버 (no JS), 150ms fade.
- **Slot list scroll**: 패널 내부 `max-height: 540px; overflow-y: auto`. 커스텀 스크롤바 (8px gold border thumb).
- **Stat radar/bars**: 데이터 prop 변화 시 부드럽게 업데이트 (선택사항: react-spring).
- **Page transition**: 화면 entry 시 `opacity 0 → 1` + `translateY 8 → 0` (350ms cubic-bezier(.2,.8,.2,1)) — `.page-enter` 클래스로 적용.
- **Reduced motion**: `prefers-reduced-motion` 시 모든 transition/animation 제거 권장.

## Responsive

- Desktop ≥ 1100px: 정상 2-col 레이아웃.
- 900–1100px: `analysis-grid`, `recs-grid` 1-col (사이드바 sticky 해제).
- < 900px: 검색 폼 1-col, recent grid 2-col, hero h1 52px.
- < 760px: char-header 1-col.

## Accessibility

- 모든 button 에 명확한 aria-label (특히 아이콘 only)
- `<a onClick>` 패턴 → `<Link>` 또는 `<button>` 으로 교체 (현재 prototype 코드의 임시 패턴)
- 포커스 ring: 기본 outline 유지하거나 `focus-visible` 시 1px gold ring
- 색 대비: 골드 vs panel 4.5:1 만족 확인
- 라이브 토스트: `role="status"` + `aria-live="polite"`

---

## Files in this bundle

| File | Purpose |
| --- | --- |
| `GearGap.html` | 전역 스타일 + 마운트 (앱 진입점) |
| `app.jsx` | App 셸 + Topbar + Landing + 라우팅 state |
| `analysis.jsx` | Analysis 화면 + StatRadar + StatBars + SlotList |
| `recommendations.jsx` | Recs 화면 + Tabs + BossCard + DungeonCard + GapSidebar + ItemTooltip |
| `data.js` | 모든 mock 데이터 (RECENT, CHAR, STATS, SLOTS, RAID, DUNGEONS, REALMS) |
| `screens.css` | Screen 2/3 전용 스타일 |
| `tweaks-panel.jsx` | 디자인 탐색용 — production 에서는 **제거** |

> ⚠️ `tweaks-panel.jsx` 와 `ScreenSwitcher` 핀(우측 상단), `__edit_mode_*` postMessage 코드는 디자인 탐색용 도구이므로 운영 빌드에서는 모두 제거하세요.

---

## Implementation Order (suggested)

1. Vite + React + TS 스캐폴드 → React Router 설치
2. `src/styles/tokens.css` (CSS variables) + Google Fonts import
3. `Background.tsx` + base 레이아웃 (`shell`, `topbar`, `footer`)
4. `LandingScreen` (mock data 연결)
5. `AnalysisScreen` — `CharHeader` → `StatRadar` (SVG) → `StatBars` → `SlotList`
6. `RecommendationsScreen` — Tabs → BossCard → DungeonCard → GapSidebar → ItemTooltip
7. 라우팅 통합 + 페이지 전환 애니메이션
8. 반응형 + 접근성 패스
9. (옵션) data 레이어를 `react-query` 로 교체 + API 어댑터 작성

---

문의: 프로토타입 동작 확인은 원본 `GearGap.html` 을 브라우저에서 직접 열어보면 됩니다.
