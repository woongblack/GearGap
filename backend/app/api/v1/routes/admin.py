from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

from app.core.config import settings

router = APIRouter(prefix="/admin", tags=["admin"])

_api_key_header = APIKeyHeader(name="X-Admin-Key", auto_error=False)


def require_admin_key(key: str | None = Security(_api_key_header)) -> None:
    if not settings.ADMIN_API_KEY or key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/seed/patch", dependencies=[Depends(require_admin_key)])
def seed_patch(version: str, type: str) -> dict:
    """
    패치 데이터 시드 주입 API.
    seeds/{version}/{type}.json 파일을 DB에 삽입.
    TODO: Phase 1 진입 시 구현
    """
    return {"status": "not_implemented", "version": version, "type": type}
