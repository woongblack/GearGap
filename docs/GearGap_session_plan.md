# GearGap MVP — 세션 계획

> **현재 진행도: Phase 1 MVP 완료 ✅ (2026-06-06)**
> 배포 URL: https://gear-gap-two.vercel.app
> 백엔드: https://geargap.onrender.com
> 총 8개 세션으로 완료. 다음 단계: Phase 2 (이행 추적 + RAG)

---

## 세션 2 — BiS 데이터 DB 적재 (A-2 + Ingestion) ✅ 완료 (2026-05-14)

### 산출물
- `app/constants/specs.py` — DPS_SPECS 26개 SSoT
- `app/models/popularity.py` — SpecSlotItemPopularity (Slot StrEnum, VARCHAR 길이 제약)
- `app/workers/murlok_ingestion.py` — delete-and-insert, scraped_at sync_start 통일
- `scripts/run_murlok_ingestion.py` — CLI 진입점 (--dry-run / --sleep)
- Alembic migration #2 (b005182f85d9)

### 결과
- 26/26 스펙 성공, 1,449행 적재, 4분 31초
- scraped_at DISTINCT = 1줄 (sync_start 통일 확인)
- "흑마 어둠 머리 BiS Top 5" 쿼리 정상 반환

---

## 세션 3 — Raidbots Ingestion + 도메인 모델 매핑 ✅ 완료

### 목표
시즌/레이드/던전/넴드/드롭처 메타데이터를 DB에 저장.

### 작업
1. **Raidbots fetcher 모듈 작성**
   - 이전에 만든 fetcher 코드 베이스로
   - 해시 환경변수 (`RAIDBOTS_HASH`)
   - 10초 throttle

2. **DTO + Mapper**
   - InstanceDTO, EncounterDTO, SeasonDTO
   - 실제 응답 보고 키 이름 정정 (이전엔 추정)

3. **기존 모델 활용**
   - Content (인스턴스), DropSource (넴드→아이템) 이미 있음
   - 필요시 컬럼 추가 (예: raidbots_id)

4. **RaidbotsIngestionWorker**
   - instances, seasons, encounter-names, bonuses 받기
   - upsert
   - 시즌별 활성 컨텐츠 표시 (is_active)

5. **데이터 검증**
   - 현재 시즌 인스턴스 수, 넴드 수 확인
   - "이번 시즌 레이드 보스 명단" 쿼리

### 산출물
- `app/services/raidbots_fetcher.py`
- `app/workers/raidbots_ingestion.py`
- 마이그레이션 파일 (필요시)

### 결정 포인트
- 아이템 ↔ 드롭처 매핑 어디까지 자동화 (Raidbots에 있는지 / 별도 작업 필요한지)
- 시즌 전환 시 기존 데이터 처리 (보존 / soft-delete / 삭제)

### 끝나는 신호
"흑마 어둠 BiS 트링켓 X의 드롭처" 쿼리로 인스턴스+넴드 이름 반환.

---

## 세션 4 — 조인 로직 (RoadmapService) ✅ 완료

### 목표
"캐릭터 장비 + BiS 후보 + 드롭처" 3개 데이터를 합쳐 로드맵 생성.

### 작업
1. **RoadmapService 설계**
   - 입력: 리전, 서버, 캐릭터명
   - 출력: 슬롯별 갭 + 드롭처 정보
   
2. **단계별 흐름**
   - Blizzard API로 캐릭터 장비 조회 (기존 코드 활용)
   - 스펙 식별
   - DB에서 그 스펙의 BiS 후보 조회
   - 슬롯별 비교: 현재 장비 vs BiS 후보
   - 누락된 BiS 아이템의 드롭처 조회
   - 결과 직렬화

3. **결과 스키마**
   ```python
   class SlotGap:
       slot: Slot
       current_item: ItemRef | None       # 지금 끼고 있는 거
       missing_bis: list[BiSCandidate]    # 안 끼고 있는 BiS 후보
       
   class BiSCandidate:
       item_id, item_name, popularity (count/50)
       drop_sources: list[DropSource]  # 인스턴스 + 넴드
   ```

4. **단위 테스트**
   - 흑마 어둠 캐릭터 가짜 데이터로 로드맵 생성 검증
   - 엣지: 슬롯 비어있음 / BiS 후보 0개 / 드롭처 없음

### 산출물
- `app/services/roadmap_service.py`
- `app/schemas/roadmap.py`
- 단위 테스트

### 결정 포인트
- "이미 착용 중인 아이템" 처리 (1-A 결정 반영)
- 드롭처 우선순위 (가까운 키 레벨? 모든 곳?)
- 캐싱 전략 (Blizzard API 응답을 잠깐 캐시할지)

### 끝나는 신호
함수 호출 한 번으로 완성된 로드맵 JSON 반환.

---

## 세션 5 — API 엔드포인트 + 통합 테스트 ✅ 완료

### 목표
HTTP로 로드맵 조회 가능.

### 작업
1. **FastAPI 라우터**
   - `GET /api/v1/characters/{region}/{realm}/{name}/roadmap`
   - 또는 `POST /api/v1/roadmap` (body로 정보 받음)
   
2. **에러 처리**
   - 캐릭터 없음 (404)
   - Blizzard API 실패 (502)
   - 지원 안 하는 스펙 (힐러/탱커 등) (400)
   
3. **응답 형식 표준화**
   - 에러 응답 구조
   - 데이터 갱신 시점 표시 (scraped_at)
   - 분모 정보 (top 50 기준)

4. **OpenAPI 스키마 검증**
   - 자동 생성된 /docs 확인
   - Pydantic 스키마와 일치

5. **수동 통합 테스트**
   - curl로 실제 호출
   - 본인 캐릭터로 검증
   - 응답 시간 측정

### 산출물
- `app/api/v1/routes/roadmap.py`
- OpenAPI 스펙
- 통합 테스트 결과

### 결정 포인트
- 인증 필요한가? (MVP는 X)
- Rate limiting (MVP는 X, 나중에)
- 로그 정책

### 끝나는 신호
백엔드 단독으로 사용자가 curl로 본인 로드맵 받을 수 있음. 백엔드 MVP 완료.

---

## 세션 6 — 프론트엔드 1: 입력 + API 연동 ✅ 완료

### 목표
사용자가 캐릭터 정보 입력 → 로드맵 받아오는 흐름.

### 작업
1. **입력 페이지**
   - 리전 셀렉트 (KR/US/EU/TW)
   - 서버 셀렉트 또는 입력
   - 캐릭터명 입력
   - 조회 버튼

2. **API 클라이언트**
   - 타입 정의 (백엔드 스키마와 동기화)
   - 에러 처리
   - 로딩 상태

3. **상태 관리**
   - 입력 폼 / 로딩 / 결과 / 에러
   - URL 라우팅 (캐릭터별 URL?)

4. **기본 결과 렌더링**
   - JSON 그대로 표시 (디자인은 다음 세션)
   - 흐름 검증용

### 산출물
- 입력 페이지 컴포넌트
- API 클라이언트 모듈
- 상태 관리 코드

### 결정 포인트
- 라우팅: `/character/{region}/{realm}/{name}` SEO 친화 / `?` 쿼리 파라미터?
- 서버 셀렉트: 하드코딩 명단 / Blizzard API 동적 조회?
- 디자인 시스템 (기존에 뭐 쓰고 있는지 확인 필요)

### 끝나는 신호
사용자가 캐릭터명 넣으면 로드맵 데이터가 화면에 (못생기게라도) 떠 있음.

---

## 세션 7 — 프론트엔드 2: 로드맵 시각화 ✅ 완료 (2026-05-17)

### 산출물
- 슬롯 갭 테이블: 골드 좌측 바(갭), dim+✓(BiS), 슬롯명 타이틀 케이스
- 행 접기/펼치기: 갭=기본 펼침, BiS=기본 접힘, chevron 토글
- Top 3 BiS 후보: count/total_sample 진행 바 + 퍼센트
- CharHeader: ApiRoadmapOut 타입으로 교체 (class_name, spec_name, name, realm, scraped_at, 갭 슬롯 수)
- 아이템 아이콘: Wowhead widget 포기 → Blizzard media API → items.icon_url → `<img>` 직접 렌더링
  - Migration #5 (a3f8e1c92b74): items.icon_url 컬럼 추가
  - scripts/fetch_item_icons.py: 432개 전부 OK
- 드롭처 칩: instance / encounter 두 줄 레이아웃 + ellipsis
- 테이블 컬럼 비율 고정 (10/25/40/25%), overflow 방지

### 커밋
- e5bf198: feat(backend): add icon_url to items, fetch from Blizzard media API
- dee99da: feat(frontend): slot gap table design, item icons, dropsource layout
- 81b3670: feat(i18n): Korean localization for dungeons, raids, and encounter names

### 한글화 범위
- contents.name_kr: 레이드 4개 + 던전 11개 (15개)
- encounters.name_kr: 레이드 넴드 9개 (The Voidspire 6 + The Dreamrift 1 + March on Quel'Danas 2)
- RoadmapService: COALESCE(name_kr, name_en) 적용 → 한글 우선, 영문 폴백
- 던전 넴드 한글화: 미완 (인게임 확인 후 seed_encounter_name_kr.py에 추가)
- 아이템명 한글화: 별도 태스크 (배포 후 진행)
- Alembic migration #6 (b7d4c2e91a05): encounters.name_kr 컬럼 추가

### 끝나는 신호
드롭처 칩 한글 인스턴스명 + 레이드 넴드 한글명 정상 표시. ✅

### 미해결 → 해결됨
- Wowhead widget 인라인 아이콘 → Blizzard API fetch로 완전 해결 ✅
- 가로 스크롤 → table-layout: fixed + 컬럼 비율 + ellipsis 해결 ✅

---

## 세션 8/9 — 마무리: 배포 + 검증 ✅ 완료 (2026-06-06)

### 목표
실제 사용자(우선 본인)가 인터넷으로 접근 가능.

### 배포 스택 (확정)
- Frontend: Vercel → https://gear-gap-two.vercel.app
- Backend: Render → https://geargap.onrender.com
- DB: Supabase PostgreSQL ✅ 완료

### 배포 체크리스트

#### 1단계: Supabase 셋업 ✅ 완료 (2026-05-27)
- [x] Supabase 프로젝트 생성
- [x] DATABASE_URL → `postgresql+psycopg://` 형식으로 교체
- [x] `alembic upgrade head` — migration 6개 적용 완료

#### 2단계: 데이터 재적재 ✅ 완료 (2026-05-27)
- [x] `insert_patch_version.py` — 12.0.5 (raidbots 전에 선행 필요)
- [x] `run_raidbots_ingestion.py` — contents 16, encounters 56, items 432, drops 447
- [x] `run_murlok_ingestion.py` — spec_slot_item_popularity 1,408행
- [x] `fetch_item_icons.py` — icon_url 432/432 OK
- [x] `seed_content_name_kr.py` — 15개
- [x] `seed_encounter_name_kr.py` — 9개

#### 3단계: 서비스 배포 ✅ 완료 (2026-06-06)
- [x] Render — FastAPI 서비스 배포 완료, `/health` 200 확인
  - 환경변수: DATABASE_URL, BLIZZARD_CLIENT_ID/SECRET, ADMIN_API_KEY 설정
  - 이슈: `beautifulsoup4`, `lxml` pyproject.toml 누락 → 추가 완료
- [x] Vercel — 프론트엔드 배포 완료 (VITE_API_URL=https://geargap.onrender.com)
  - 이슈: `CharHeader` prop 타입 불일치 → 수정 완료
- [x] CORS — `*.vercel.app` 패턴으로 정상 동작 확인

#### 4단계: 자동화 ✅ 완료 (2026-06-06)
- [x] GitHub Actions 크론: Murlok ingestion 1일 1회 (KST 00:00)
  - Secret: `DATABASE_URL` (Session Pooler, 포트 5432)
  - 이슈: setuptools flat-layout → `requirements.txt` 방식으로 변경
  - 이슈: Supabase DB 복원 중 연결 실패 → 복원 후 정상화
- [x] Render keep-alive — cold start 감수하기로 결정 (무료 플랜)

#### 5단계: 검증 ✅ 완료 (2026-06-06)
- [x] 본인 캐릭터로 End-to-End 검증 (검색 → 아이콘 → 드롭처 한글명) — 200 OK 확인
- [x] 배포 URL 공유 가능 상태 확인 — https://gear-gap-two.vercel.app

### 세션 중 추가 작업 (2026-06-06)
- mock Recent Searches → localStorage 기반 실제 검색 기록으로 교체
- Admin 엔드포인트 API Key 인증 추가 (`X-Admin-Key` 헤더)
- 미사용 컴포넌트 삭제: `MetaDrawer.tsx`, `MetaRibbon.tsx`
- setuptools 패키지 디스커버리 설정 (`[tool.setuptools.packages.find]`, `[build-system]`)

### 작업
1. **백엔드 배포**
   - 호스팅 선택 (Railway / Fly.io / Render / 직접 서버)
   - 환경변수 설정 (시크릿 안전하게)
   - SQLite → Postgres (Supabase) 마이그레이션
   - 도메인 (선택)

2. **프론트엔드 배포**
   - Vercel / Netlify / Cloudflare Pages
   - API URL 환경변수

3. **Ingestion 스케줄링**
   - Murlok 1일 1회 자동 실행
   - 크론 / 외부 스케줄러 (cron-job.org / GitHub Actions)

4. **본인 캐릭터로 End-to-End 검증**
   - 실제 URL로 접속
   - 로드맵 정상 표시
   - 데이터 갱신 확인

5. **README**
   - 프로젝트 소개
   - 사용법
   - 데이터 출처 명시 (Murlok에 대한 감사)

### 산출물
- 배포된 URL
- README
- 운영 가이드

### 결정 포인트
- 도메인 살 건지
- 베타 공개 범위 (본인만 / 지인 / 공개)
- 분석 도구 (필요 시)

### 끝나는 신호
**"https://geargap.example.com 가서 캐릭터 검색해봐" 라고 친구한테 링크 보낼 수 있음.** MVP 완료.

---

## 🎯 세션 외 — 중간에 들어갈 수 있는 것들

### 작은 작업 (10~30분, 빈 시간에)
- Murlok robots.txt 재확인 (정기)
- 26 스펙 명단 변경 시 업데이트 (영웅특성 추가 등)
- Wowhead 아이콘 캐싱
- 에러 모니터링 (Sentry 같은 거)

### 미정 작업 (Phase 2 검토 시)
- 영문/한국어 다국어
- 캐릭터 즐겨찾기 (DB에 저장)
- 이행 추적 (장비 변화 기록)
- 힐러/탱커 지원
- 레이드 BiS (현재 M+만)

---

## 📊 진척도 시각화

```
세션 1 ✅: Phase 0 + MurlokScraper + 청소           [████████░░░░░░░░░░░░░░░░░░░░] 35%
세션 2 ✅: BiS DB 적재                              [██████████░░░░░░░░░░░░░░░░░░] 45%
세션 3 ✅: Raidbots ingestion                       [████████████░░░░░░░░░░░░░░░░] 55%
세션 4 ✅: RoadmapService                           [██████████████░░░░░░░░░░░░░░] 65%
세션 5 ✅: API + 통합                               [████████████████░░░░░░░░░░░░] 75%
세션 6 ✅: 프론트 입력+연동                          [██████████████████░░░░░░░░░░] 85%
세션 7 ✅: 프론트 시각화                             [████████████████████████░░░░] 95%
세션 8 ✅: 배포+검증                                [████████████████████████████] 100%
```

---

## ⚠️ 리스크 + 대응

| 리스크 | 발생 시점 | 대응 |
|---|---|---|
| Murlok HTML 구조 변경 | 세션 2 이후 언제든 | canary 검증 + WCL API 폴백 |
| Raidbots 해시 변경 | 세션 3 | /developers 파싱 자동화 |
| Blizzard API rate limit | 세션 5 이후 | 캐시 + 백오프 |
| 디자인 시스템 결정 지연 | 세션 7 | 기존 코드베이스 컨벤션 따르기 |
| 배포 환경 변수 누락 | 세션 8 | .env.example 미리 작성 |

---

## 💡 매 세션 시작 시 체크리스트

```
□ 이전 세션 산출물 정상 동작 확인 (sanity check)
□ briefing.md + 진행 상태 메모 Claude Code에 전달
□ 오늘 세션 목표 한 줄 명시
□ 결정 포인트 미리 알려주기 (즉답 못 하면 미루기)
□ 끝나는 신호 정의
□ 세션 끝나면 다음 세션 시작점 메모 업데이트
```

### "2026-05-24 — 세션 8 1단계 완료: Supabase 프로젝트 생성, GitHub 연결, DATABASE_URL 확보