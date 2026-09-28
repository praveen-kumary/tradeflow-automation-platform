from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check() -> dict:
    settings = get_settings()
    return {
        "ok": True,
        "environment": settings.app_env,
        "trading_mode": settings.trading_mode,
        "broker": settings.broker_provider,
    }

