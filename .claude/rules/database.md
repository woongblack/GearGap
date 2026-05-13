# Database 기준 (PostgreSQL / Supabase → 개발 중 SQLite)

## 개발 환경

- 개발: SQLite (`backend/geargap_dev.db`) — `DATABASE_URL=sqlite:///./geargap_dev.db`
- 프로덕션: Supabase PostgreSQL (Phase 1 완료 후 전환)
- 마이그레이션: Alembic (`backend/alembic/versions/`)

## ERD 개요

```
패치 관리:   PATCH_VERSIONS
캐릭터:      CHARACTERS, CHARACTER_EQUIPMENT, CHARACTER_STATS
메타:        CLASSES, SPECS
정적 데이터: ITEMS, CONTENTS, DROP_SOURCES      ← patch_version + is_active
BiS 데이터:  SPEC_SLOT_ITEM_POPULARITY           ← Murlok 크롤링 결과
```

## 핵심 패턴

### patch_version 관리

- `ITEMS`, `CONTENTS`, `DROP_SOURCES`는 `patch_version FK` + `is_active boolean` 필수
- 현재 패치 데이터: `is_active = true`
- 이전 패치 데이터: `is_active = false` (보존, 삭제 금지 — 검증/디버깅용)

### 캐릭터 캐싱

- `last_synced_at` 기준 10분 이내 → DB 반환 (Blizzard API 호출 생략)
- CHARACTERS는 `patch_version` 없음 (캐릭터는 항상 최신 상태 추적)

### SPEC_SLOT_ITEM_POPULARITY 패턴

- `scraped_at` 기준 1일 1회 갱신 (Murlok 크롤링)
- `(class_name, spec_name, content_type, slot)` 조합으로 조회
- `total_sample` 항상 50 (Murlok 기준)
- upsert 전략: **delete-and-insert (스펙 단위 트랜잭션)**
  - `BEGIN → DELETE WHERE (class, spec, content_type) → INSERT → COMMIT`
  - 26 스펙 통째로 트랜잭션 금지 (락 너무 김) — 스펙 1개 = 1 트랜잭션
- `scraped_at`: 워커 사이클 시작 시각(`sync_start`)으로 전 행 통일 — MurlokScraper 내부 값 무시

## v0.6 핵심 쿼리 패턴

```sql
-- 슬롯별 BiS 후보 조회 (특정 스펙)
SELECT slot, item_name, item_id, count, total_sample
FROM spec_slot_item_popularity
WHERE class_name = 'warlock'
  AND spec_name = 'destruction'
  AND content_type = 'mythic-plus'
ORDER BY slot, count DESC;

-- 내 장비 vs BiS 갭 (LEFT JOIN)
SELECT
    eq.slot,
    eq.item_id        AS my_item_id,
    bis.item_name     AS bis_item_name,
    bis.item_id       AS bis_item_id,
    bis.count         AS bis_count,
    bis.total_sample
FROM character_equipment eq
LEFT JOIN spec_slot_item_popularity bis
    ON bis.slot = eq.slot
    AND bis.class_name = 'warlock'
    AND bis.spec_name = 'destruction'
    AND bis.content_type = 'mythic-plus'
WHERE eq.character_id = ?
  AND eq.item_id != bis.item_id   -- 이미 BiS 착용 중이면 제외
ORDER BY bis.count DESC;

-- 활성 아이템 조회
SELECT id, name, slot FROM items
WHERE patch_version = '11.1.5' AND is_active = true;
```

## Supabase 설정 (Phase 1 이후)

- pgvector 익스텐션 활성화 (Phase 2 RAG 대비)
- Connection Pooler 사용 (Cloud Run 잦은 연결 대응)
- RLS(Row Level Security): Phase 2 사용자 인증 시 적용

## 마이그레이션

- Alembic 사용
- 마이그레이션 파일은 `backend/alembic/versions/` 에 보관
- 프로덕션 마이그레이션 전 반드시 로컬(SQLite) 검증

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
- `is_active` 없이 정적 데이터 조회 금지
- 시드 데이터를 DB에 직접 수동 편집하지 않고 반드시 JSON 파일 → 시드 스크립트 경유
