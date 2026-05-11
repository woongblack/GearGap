# 인프라 기준 (Vercel + GCP Cloud Run + Supabase)

## Tri-Layer Architecture

```
Frontend  →  Vercel (geargap.app)
Backend   →  GCP Cloud Run (api.geargap.app, asia-northeast3)
Database  →  Supabase (PostgreSQL + pgvector)
```

## 환경 변수 관리 원칙

- 로컬: `.env.local` (git 추적 금지)
- 프로덕션: GCP Secret Manager
- `.env` 파일에 실제 secrets 절대 커밋 금지

| 변수 | 위치 | 용도 |
|------|------|------|
| `VITE_API_URL` | Vercel 환경변수 | 프론트 → 백엔드 URL |
| `DATABASE_URL` | GCP Secret Manager | Supabase 연결 |
| `BLIZZARD_CLIENT_ID` | GCP Secret Manager | Blizzard API 인증 |
| `BLIZZARD_CLIENT_SECRET` | GCP Secret Manager | Blizzard API 인증 |
| `CLAUDE_API_KEY` | GCP Secret Manager | Phase 2 |

## CORS 설정 (backend/main.py)

```python
allow_origins=[
    "https://geargap.app",
    "https://*.vercel.app",   # Preview Deployments
    "http://localhost:5173",  # 로컬 개발
]
```

- 개발 중 `allow_origins=["*"]` 는 임시 허용, 배포 전 제한 필수

## CI/CD

- Frontend: git push → Vercel 자동 배포 (~30초~1분)
- Backend: git push → GitHub Actions → Cloud Run (~3~5분)
- PR 시 Vercel Preview URL 자동 생성

## Cloud Run 설정

- Region: `asia-northeast3` (서울) — 한국 와우 유저 응답 속도 최적
- Cold Start 1~3초 발생 가능 → Loading 화면 4단계 진행 텍스트로 UX 보완
- Min Instances = 0 (무료 티어), 트래픽 증가 시 유료 전환 검토
- Dockerfile 필수, `PORT` 환경변수 사용 (`--port ${PORT:-8080}`)

## Docker (backend)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
```

`.dockerignore`: `__pycache__`, `*.pyc`, `.env`, `.venv`

## 비용 목표

- Phase 1: ~1만원/년 (도메인만)
- Phase 2: ~월 1~3만원 (Claude API 추가)
- 예산 알림: GCP 콘솔에서 설정 (폭탄 방지)
