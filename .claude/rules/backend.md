# Backend 코딩 기준 (FastAPI / Python)

## 레이어 구조

```
Router (HTTP 진입점)
  → Service (비즈니스 로직)
    → Repository (데이터 접근)
      → Models (DB 스키마)
```

- 라우터에 비즈니스 로직 작성 금지
- 에러 처리는 중앙화된 exception handler로
- 의존성 주입(Dependency Injection) 활용

## 디렉토리 구조

```
backend/
├── app/
│   ├── main.py                   # FastAPI app, CORS, lifespan
│   ├── api/
│   │   ├── deps.py               # SessionDep (DI)
│   │   └── v1/
│   │       ├── router.py         # APIRouter 집합
│   │       └── routes/
│   │           ├── characters.py # GET /api/v1/characters/{realm}/{name}
│   │           ├── efficiency.py # GET /api/v1/efficiency/{character_id}
│   │           └── admin.py      # POST /api/v1/admin/seed/patch
│   ├── core/
│   │   ├── config.py             # pydantic-settings (Settings)
│   │   └── db.py                 # SQLModel engine + get_session
│   ├── models/
│   │   ├── patch.py              # PATCH_VERSIONS
│   │   ├── character.py          # CHARACTERS, CHARACTER_EQUIPMENT, CHARACTER_STATS
│   │   ├── meta.py               # CLASSES, SPECS
│   │   ├── item.py               # ITEMS, CONTENTS, DROP_SOURCES
│   │   └── simulation.py         # SIMULATION_RESULTS
│   ├── schemas/
│   │   ├── character.py          # CharacterPublic (response)
│   │   └── efficiency.py         # EfficiencyResponse, EvidenceDetail, WeightParams
│   ├── services/
│   │   ├── blizzard.py           # Blizzard API client (OAuth + 캐릭터 조회)
│   │   └── efficiency.py         # 효율 점수 계산 엔진
│   └── repositories/
│       └── character_repo.py     # get_cached_character, upsert_character
├── alembic/
│   ├── env.py
│   └── versions/
├── tests/
├── main.py                       # uvicorn main:app 로컬 진입점
├── Dockerfile
├── .env.example
├── alembic.ini
└── pyproject.toml
```

로컬 실행: `uvicorn main:app --reload` (backend/ 에서)
프로덕션: `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}`

## Blizzard API

- OAuth 토큰은 메모리 캐싱 (만료 60초 전 갱신)
- 캐릭터 데이터: 10분 캐시 (`last_synced_at` 기준)
- realm slug 매핑 별도 파일로 관리 (`realms.py`)
- 한국 API 엔드포인트: `https://kr.api.blizzard.com`, `namespace: profile-kr`, `locale: ko_KR`

## 보안

- secrets은 환경 변수로만 관리 (`.env` 파일에 직접 작성 금지, 프로덕션은 GCP Secret Manager)
- SQL은 parameterized query만 사용 (injection 방지)
- CORS는 허용 origin 명시 (`allow_origins=["*"]` 는 개발 중에만)

## 환경 변수

```
DATABASE_URL        # Supabase connection string
BLIZZARD_CLIENT_ID
BLIZZARD_CLIENT_SECRET
CLAUDE_API_KEY      # Phase 2
```

## 에러 응답 형식

```python
raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없어요")
```

- 사용자 향 메시지는 한국어
- detail은 간결하게 (내부 에러 스택 노출 금지)

## 코드 품질

- 타입 힌트 필수 (Python 3.11+)
- Pydantic 모델로 request/response 검증
- 함수 길이 50줄 이하 목표
- 테스트: pytest, 외부 API는 mock 처리

## 금지 패턴

- ORM 객체를 비동기 컨텍스트 간에 공유하지 않음
- 라우터에서 직접 DB 쿼리 작성 금지
- `SELECT *` 사용 금지 (컬럼 명시)
