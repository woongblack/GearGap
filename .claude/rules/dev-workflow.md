# 개발 워크플로우

## 로컬 실행

```bash
# Frontend (localhost:5173)
cd frontend
npm install
npm run dev

# Backend (localhost:8000)
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 프로젝트 구조

```
GearGap/
├── frontend/      # React + Vite + TypeScript
├── backend/       # FastAPI + Python
├── docs/          # 레거시 PRD 문서
├── capture/       # UI 스크린샷 (참고용)
└── .claude/
    ├── settings.json
    ├── settings.local.json
    └── rules/
```

Obsidian 문서 (기획/설계): `C:\Users\Windows10\Documents\ObsidianVault\Projects\GearGap\`

## 브랜치 전략

- `main`: 배포 가능한 상태 유지
- `feat/`: 기능 개발
- `fix/`: 버그 수정
- `chore/`: 설정/인프라 변경

## 개발 순서 원칙

1. 외부 의존성 먼저 검증 (bloodmallet 접근 가능 여부 등)
2. DB 스키마 → 백엔드 API → 프론트엔드 순
3. 각 Phase 완료 후 dogfooding (본인 흑마 캐릭터로 실사용) 검증
4. Phase 1 안 되면 Phase 2 설계 시작 금지

## 시드 데이터 작업

```bash
# 패치 시드 주입 (관리자 API)
POST /admin/seed/patch
Body: { "version": "11.1.5", "type": "items" }
```

## 디버깅

1. 재현 가능한 케이스 먼저 만들기
2. 근본 원인 파악 (증상 임시 처리 금지)
3. 최소한의 수정만
4. 외부 API 에러는 로그에 상태 코드 + 응답 body 기록

## 테스트

- API 테스트: pytest
- 외부 API(Blizzard, bloodmallet): mock 처리
- DB 연동 테스트: Supabase 로컬 또는 테스트 DB 사용
