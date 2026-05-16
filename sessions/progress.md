## 2026-05-17 — 세션 6 완료 ✅

### 상태
프론트엔드 로드맵 API 연동 완료. 캐릭터명 입력 → 슬롯 갭 테이블 브라우저에서 확인.

### 산출물
- `api/types.ts`: v0.5 타입 제거, 로드맵 타입 4개 추가 (ApiRoadmapOut 등)
- `api/client.ts`: getRoadmap(realm, name, contentType?) 추가
- `App.tsx`: LoadingScreenWrapper — getRoadmap() 호출, 성공 시 state 전달, 실패 시 /errors
- `AnalysisScreen.tsx`: location.state.roadmap 읽기, 슬롯 갭 테이블 렌더링 (갭 슬롯 우선, BiS 슬롯 하단)

### 끝나는 신호 달성
캐릭터명 입력 → LoadingScreen 애니메이션 → AnalysisScreen 슬롯 갭 테이블 표시 ✅

### 다음 세션 7 — 디자인
- AnalysisScreen 슬롯 갭 테이블 시각 디자인
- CharHeader 컴포넌트 연동 (roadmap → CharProfile 매핑)
- 슬롯별 갭 강조 (BiS vs 갭 시각 구분)
- 드롭처 레이아웃 정리

---

## 2026-05-16 — 세션 5 완료 ✅

### 상태
Roadmap API 엔드포인트 완성. Blizzard API 연동 + 캐싱 + 에러 표준화.

### 산출물
- GET /api/v1/characters/{realm}/{name}/roadmap
  - query: content_type (Literal["mythic-plus"]), spec_name (Optional)
  - Blizzard API miss → profile + equipment 조회 + DB upsert
  - 캐시 히트 → DB 반환 (Blizzard 호출 생략)
  - 비DPS 스펙 → 404, Blizzard 타임아웃 → 502
- COALESCE 버그 수정 (roadmap_repo.py:34)
  - `COALESCE(i.name, ce.item_name)` — items 테이블 미존재 시 Blizzard 이름으로 폴백
- alembic head: 004b09dd9606 (drop item_id FK, add item_name to character_equipment)

### 끝나는 신호 달성
- 4개 테스트 전부 통과
  1. 첫 번째 호출 (Blizzard API miss): 4407ms, slots=14, my_item_name 14/14 filled ✅
  2. 두 번째 호출 (캐시 히트): 2130ms ✅
  3. 잘못된 content_type=invalid → 422 ✅
  4. COALESCE 수정 후 재검증: my_item_name null=0 ✅

### 핵심 결정
- is_bis=False 전부 → 정상 동작
  * BiS DB: 12.x 패치 아이템 (Abyssal Immolator's 세트 등, item_id 25xxxx)
  * 캐릭터 장비: 11.x 시즌 아이템 → 매칭 없음
- 캐싱 로직: 10분 이내 last_synced_at → Blizzard API 생략
- spec_name query param: 없으면 active_spec 사용

### 미해결 태스크 (별도, 세션 8 전 처리 필요)
- 제작템/외부 아이템 186개 보완 (현재 source_type="unknown")
  * Raidbots crafting.json 또는 Blizzard Game Data API
  * 완료 기준: ssip BiS 후보 전체가 items 테이블에 존재

### 다음 세션 6 — 프론트엔드 입력+연동
- LandingScreen → 캐릭터 입력 UI
- /loading → AnalysisScreen 라우팅
- /c/{realm}/{name}/roadmap 엔드포인트 연결
- BiS 갭 대시보드 렌더링

---

## 2026-05-XX — 세션 4 완료 ✅

### 상태
RoadmapService 구현 완료. 함수 호출로 로드맵 JSON 반환.

### 산출물
- app/schemas/roadmap.py (4개 스키마)
- app/repositories/roadmap_repo.py (2개 쿼리)
- app/services/roadmap.py (get_roadmap + _aggregate_bis)

### 끝나는 신호 달성
get_roadmap(warlock/destruction) → RoadmapOut(slots=14, 12122 bytes)
7개 검증 전부 통과.

### 핵심 결정
- is_bis: 전체 후보 1위 기준 (source_type 무관)
- bis_candidates: 서비스 전체 반환, UI에서 Top N
- unknown 아이템: 포함 + drop_sources=[]
- 비DPS 스펙: ValueError → 라우터에서 404 변환

### 미해결 태스크 (세션 8 전 처리 필요)
- 제작템/외부 아이템 186개 보완 (현재 source_type="unknown")
  * Raidbots crafting.json 또는 Blizzard Game Data API

### 다음 세션 5 — API 엔드포인트
GET /api/v1/characters/{region}/{realm}/{name}/roadmap
Blizzard API 연결 + content_type validation + 에러 표준화

### [별도 태스크 — 제작템/외부 아이템 보완]
우선순위: Post-세션 4, 세션 8 이전
내용: Raidbots equippable-items.json 외 소스에서
     제작 티어셋 등 186개 누락 아이템 적재
후보 소스:
  - Raidbots 다른 엔드포인트 (crafting 관련)
  - Wowhead 아이템 DB
  - Blizzard Game Data API (item-search)
완료 기준: ssip BiS 후보 전체가 items 테이블에 존재

세션 8 배포 구성 (확정):
- 프론트: Vercel
- 백엔드: Render (무료, 콜드 스타트 감수)
- DB: Supabase (Postgres)
- 크론: GitHub Actions (Murlok ingestion 1일 1회 + Render keep-alive)
- 비용: $0/월