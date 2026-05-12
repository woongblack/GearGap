from fastapi import APIRouter

from app.api.v1.routes import admin, characters

router = APIRouter()
router.include_router(characters.router)
router.include_router(admin.router)
