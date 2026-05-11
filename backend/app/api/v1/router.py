from fastapi import APIRouter

from app.api.v1.routes import admin, characters, efficiency

router = APIRouter()
router.include_router(characters.router)
router.include_router(efficiency.router)
router.include_router(admin.router)
