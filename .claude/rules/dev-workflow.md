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
venv\Scripts\activate           # Windows
# source venv/bin/activate      # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

## 프로젝트 구조

```
GearGap/
├── frontend/      # React + Vite + TypeScript
├── backend/       # FastAPI + Python
├── docs/          # 작업 지시서 / 브리핑 문서
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

1. 외부 의존성 먼저 검증 (PoC 완료 후 다음 단계)
2. DB 스키마 → 백엔드 API → 프론트엔드 순
3. 각 Phase 완료 후 dogfooding (본인 흑마 캐릭터로 실사용) 검증
4. Phase 1 안 되면 Phase 2 설계 시작 금지

## 협업 규칙 (Claude Code 행동 기준)

### 다음 단계 결정
- 한 작업이 끝나면 "다음은 X로 갑니다" 선언 금지
- 옵션을 제시하고 사용자 결정을 기다릴 것
- 결정 안 된 사항(DB 종류, 아키텍처 방향 등)이 있으면 먼저 질문

### 요청 항목 누락 금지
- 사용자 메시지에 번호 붙은 질문이나 체크리스트가 있으면 전부 응답한 후 다음 진행
- "진행할까요?" 전에 요청된 보고/공유 항목 먼저 완료

### 데이터 소스 변경 원칙
- PoC 한 번도 안 해보고 데이터 소스 갈아엎지 말 것
- 더 좋아 보이는 소스 발견해도 현재 결정을 먼저 검증한 후 논의
- **Archon.gg 크롤링 절대 금지** — RPGLogs ToS 명시적 금지 ("you will not perform any data-mining, scraping, crawling")

## 보안 규칙

- `.env` 파일 내용을 채팅 출력에 절대 포함하지 말 것
- diff나 보고 시 시크릿 라인은 `BLIZZARD_CLIENT_SECRET=***` 형식으로 마스킹
- 환경변수 수정 시 변경 사실만 보고, 값 노출 금지
- 토큰 / 패스워드 / API 키를 채팅창에 입력하지 말 것 (사용자 안내 포함)

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
- 외부 API(Blizzard, Murlok): mock 처리
- DB 연동 테스트: SQLite 로컬 (개발) / Supabase (프로덕션)
