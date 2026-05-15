from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 모든 SQLModel 테이블 메타데이터 등록 (FK resolve에 필요)
    from app.models import character, item, meta, patch, popularity  # noqa: F401
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/health/live")
def liveness() -> dict:
    return {"status": "ok"}
