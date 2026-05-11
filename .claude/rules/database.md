# Database 기준 (PostgreSQL / Supabase)

## ERD 개요 — 10개 테이블 (Phase 1)

```
패치 관리:   PATCH_VERSIONS
캐릭터:      CHARACTERS, CHARACTER_EQUIPMENT, CHARACTER_STATS
메타:        CLASSES, SPECS
정적 데이터: ITEMS, CONTENTS, DROP_SOURCES   ← patch_version + is_active
시뮬:        SIMULATION_RESULTS              ← patch_version + is_latest
```

## 핵심 패턴

### patch_version 관리

- `ITEMS`, `CONTENTS`, `DROP_SOURCES`는 `patch_version FK` + `is_active boolean` 필수
- 현재 패치 데이터: `is_active = true`
- 이전 패치 데이터: `is_active = false` (보존, 삭제 금지 — 검증/디버깅용)

### is_active vs is_latest 구분

- `is_active`: 패치 단위 활성 여부 (ITEMS, CONTENTS, DROP_SOURCES)
- `is_latest`: 동일 패치 내 최신 시뮬 여부 (SIMULATION_RESULTS만)
- 혼용 금지 — 의미가 다름

### 캐릭터 캐싱

- `last_synced_at` 기준 10분 이내 → DB 반환 (Blizzard API 호출 생략)
- CHARACTERS는 `patch_version` 없음 (캐릭터는 항상 최신 상태 추적)

## 효율 점수 쿼리 흐름

```sql
-- 활성 아이템 조회
WHERE patch_version = '11.1.5' AND is_active = true

-- 최신 시뮬 결과
WHERE spec_id = ? AND item_id = ? AND is_latest = true

-- 효율 점수 계산 (Python에서)
score = (dps_gain * w_dps) / (avg_clear_minutes * w_time) * (drop_rate * w_prob)
```

## Supabase 설정

- pgvector 익스텐션 활성화 (Phase 2 RAG 대비)
- Connection Pooler 사용 (Cloud Run 잦은 연결 대응)
- RLS(Row Level Security): Phase 2 사용자 인증 시 적용

## 마이그레이션

- Alembic 사용
- 마이그레이션 파일은 `backend/alembic/versions/` 에 보관
- 프로덕션 마이그레이션 전 반드시 로컬 검증

## 시드 데이터 구조

```
backend/seeds/
├── 11.1.5/
│   ├── items.json
│   ├── contents.json
│   ├── drop_sources.json
│   └── classes_specs.json
└── scripts/
    └── seed_patch.py
```

- 시드 파일은 git에 버전 관리 (패치별 보존)
- 주입 API: `POST /admin/seed/patch` (관리자 전용)

## 금지 패턴

- `SELECT *` 사용 금지
- `is_active`/`is_latest` 없이 정적 데이터/시뮬 데이터 조회 금지
- 시드 데이터를 DB에 직접 수동 편집하지 않고 반드시 JSON 파일 → 시드 스크립트 경유
