from fastapi import APIRouter

from app.api import health, transform

router = APIRouter()
router.include_router(health.router, tags=["health"], prefix="/api")
router.include_router(transform.router, tags=["transform"], prefix="/api")
