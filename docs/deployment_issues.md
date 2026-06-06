# 배포 트러블슈팅 기록 (2026-06-06)

세션 8 배포 과정에서 발생한 문제와 해결 방법 정리.

---

## Vercel (프론트엔드)

### 1. TypeScript 빌드 오류 — CharHeader prop 타입 불일치

**증상**
```
error TS2322: Type '{ char: CharProfile; }' is not assignable to type 'IntrinsicAttributes & CharHeaderProps'.
Property 'char' does not exist on type 'IntrinsicAttributes & CharHeaderProps'.
Command "npm run build" exited with 2
```

**원인**
`CharHeader` 컴포넌트가 `{ roadmap: ApiRoadmapOut; name: string; realm: string }` props를 받도록 업그레이드됐는데, `RecommendationsScreen`이 이전 방식인 `char={CHAR}` 로 넘기고 있었음.

**해결**
`RecommendationsScreen`은 전체가 mock 데이터 기반이라 `CharHeader` import 및 사용 코드 제거.

---

### 2. mock Recent Searches 카드 클릭 시 실제 API 호출

**증상**
랜딩 화면의 "Recent Searches" 카드(mock 데이터 "아즈모단")를 클릭하면 실제 Blizzard API를 호출해 "캐릭터를 찾을 수 없습니다" 에러 발생.

**원인**
`CharacterCard` onClick이 mock 캐릭터명으로 `/c/{realm}/{name}` 으로 바로 navigate. 실제 없는 캐릭터라 404.

**해결**
mock Recent Searches 섹션 제거 → localStorage 기반 실제 검색 기록으로 교체.
- 검색 성공 시 `{name, realm, searchedAt}` 저장 (최대 5개)
- 랜딩 화면에서 localStorage 읽어 표시
- 기록 없으면 섹션 자체 숨김

---

## Render (백엔드)

### 3. DATABASE_URL 형식 오류

**증상**
```
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL from given URL string
```

**원인**
Render 환경변수에 `postgresql://...` 형식으로 입력. SQLAlchemy + psycopg3 조합은 `postgresql+psycopg://` 드라이버 지정자가 필요.

**해결**
`postgresql://` → `postgresql+psycopg://` 로 변경.

---

### 4. beautifulsoup4 / lxml 모듈 없음

**증상**
```
ModuleNotFoundError: No module named 'bs4'
Application startup failed. Exiting.
```

**원인**
`murlok.py`가 `beautifulsoup4`를 import하는데 `pyproject.toml` dependencies에 누락됨. 로컬에는 설치돼 있어서 발견 못 함.

**해결**
`pyproject.toml`에 추가:
```toml
"beautifulsoup4>=4.12.0",
"lxml>=5.0.0",
```

---

## GitHub Actions + Supabase (Murlok Ingestion 크론)

### 5. setuptools flat-layout 패키지 디스커버리 오류

**증상**
```
error: Multiple top-level packages discovered in a flat-layout: ['app', 'data', 'alembic'].
ERROR: Failed to build installable wheels for some pyproject.toml based projects
```

**원인**
GitHub Actions에서 `pip install .` 실행 시, `backend/` 디렉토리에 `app/`, `data/`, `alembic/` 세 개의 최상위 패키지가 있어 setuptools가 자동 감지를 거부.
Dockerfile은 `pyproject.toml`만 먼저 복사 후 설치해서 이 문제가 없었음.

**해결**
`pip install .` 방식 포기 → `requirements.txt` 별도 관리 후 `pip install -r requirements.txt` 사용.
`pyproject.toml`에 `[build-system]` 및 `[tool.setuptools.packages.find]` 추가는 캐시 문제로 효과 없었음.

---

### 6. pip 캐시로 인해 이전 명령어가 계속 실행되는 현상

**증상**
workflow 파일을 수정해도 Actions에서 계속 `Run pip install .` 실행.

**원인**
`setup-python@v5`의 `cache: 'pip'` 옵션이 이전 실행의 캐시를 복원하면서 이전 명령어가 재실행되는 것으로 추정.

**해결**
workflow에서 `cache: 'pip'` 옵션 제거.

---

### 7. Transaction Pooler(6543) 장시간 연결 타임아웃

**증상**
26개 스펙 ingestion 중 13번째 스펙부터 DB 연결 실패:
```
FATAL: (ENOTFOUND) tenant/user postgres.gegnhrmggrhlhzujnnom not found
```

**원인**
Supabase Transaction Pooler(포트 6543)는 단발성 웹 요청용으로 설계됨. Ingestion은 26개 스펙 × 10초 슬립 = 4분 이상 소요되므로 연결이 중간에 끊김.

**해결**
GitHub Actions Secret의 `DATABASE_URL` 포트를 `6543` → `5432`(Session Pooler)로 변경.
- Render 환경변수는 단발성 요청이므로 6543 유지

---

### 8. Supabase DB 복원 중 연결 실패

**증상**
포트 변경 후에도 1번 스펙부터 즉시 연결 실패.

**원인**
Supabase가 DB 복원(Restoration) 중이어서 모든 연결 거부. Supabase 대시보드에 "Restoration in progress" 표시.

**해결**
복원 완료(Status: Healthy) 후 재실행. 자동 해결.

---

## 설정 결정 사항

| 항목 | 결정 | 이유 |
|------|------|------|
| Render keep-alive | 미설정 | GitHub Actions 분 소모(월 ~3,000분) 대비 효과 낮음, cold start 감수 |
| Admin API 인증 | `X-Admin-Key` 헤더 | 단순하고 충분한 MVP 수준 보안 |
| Render DB URL 포트 | 6543 유지 | 단발성 요청은 Transaction Pooler가 적합 |
| GitHub Actions DB URL 포트 | 5432 사용 | 장시간 스크립트는 Session Pooler가 적합 |
