from fastapi import APIRouter

router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/active")
async def active_trades() -> list[dict]:
    return [
        {
            "symbol": "RELIANCE",
            "side": "BUY",
            "entry": 2840.5,
            "current": 2862.2,
            "stopLoss": 2818.0,
            "target": 2895.0,
            "reason": "ORB Breakout + RSI > 55 + EMA20 confirmation",
        }
    ]


@router.get("/equity-curve")
async def equity_curve() -> list[dict]:
    return [
        {"date": "2026-04-22", "equity": 1_000_000},
        {"date": "2026-04-23", "equity": 1_006_400},
        {"date": "2026-04-24", "equity": 1_003_700},
        {"date": "2026-04-27", "equity": 1_012_900},
    ]

