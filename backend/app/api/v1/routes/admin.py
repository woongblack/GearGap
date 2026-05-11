from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/seed/patch")
def seed_patch(version: str, type: str) -> dict:
    """
    패치 데이터 시드 주입 API.
    seeds/{version}/{type}.json 파일을 DB에 삽입.
    TODO: Phase 1 진입 시 구현
    """
    return {"status": "not_implemented", "version": version, "type": type}
