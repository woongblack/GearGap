from fastapi import APIRouter, HTTPException, Query

from app.api.deps import SessionDep
from app.models.character import Character
from app.models.patch import PatchVersion
from app.schemas.efficiency import EfficiencyResponse, WeightParams
from app.services.efficiency import get_efficiency_candidates
from sqlmodel import select

router = APIRouter(prefix="/efficiency", tags=["efficiency"])


@router.get("/{character_id}", response_model=EfficiencyResponse)
def get_efficiency(
    character_id: int,
    session: SessionDep,
    w_dps: float = Query(default=1.0, ge=0.5, le=2.0),
    w_time: float = Query(default=1.0, ge=0.5, le=2.0),
    w_prob: float = Query(default=1.0, ge=0.5, le=2.0),
) -> EfficiencyResponse:
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없어요")

    if not character.active_spec_id:
        raise HTTPException(status_code=400, detail="스펙 정보를 가져올 수 없어요")

    patch = session.exec(
        select(PatchVersion).where(PatchVersion.is_current == True)
    ).first()
    if not patch:
        raise HTTPException(status_code=503, detail="현재 패치 정보가 없어요")

    weights = WeightParams(w_dps=w_dps, w_time=w_time, w_prob=w_prob)
    candidates = get_efficiency_candidates(
        session, character.active_spec_id, patch.version, weights
    )

    return EfficiencyResponse(
        character_name=character.name,
        spec_name="",  # TODO: join with specs table
        patch_version=patch.version,
        weights=weights,
        candidates=candidates,
    )
