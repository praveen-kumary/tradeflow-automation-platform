from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_settings
from app.core.events import CandleEvent


def create_engine() -> AsyncEngine:
    return create_async_engine(get_settings().database_url, pool_pre_ping=True)


async def insert_candle(engine: AsyncEngine, candle: CandleEvent) -> None:
    query = text(
        """
        INSERT INTO candles (symbol, timeframe, ts, open, high, low, close, volume)
        VALUES (:symbol, :timeframe, :ts, :open, :high, :low, :close, :volume)
        ON CONFLICT (symbol, timeframe, ts) DO UPDATE SET
          open = EXCLUDED.open,
          high = EXCLUDED.high,
          low = EXCLUDED.low,
          close = EXCLUDED.close,
          volume = EXCLUDED.volume
        """
    )
    async with engine.begin() as conn:
        await conn.execute(query, candle.model_dump())


async def fetch_recent_candles(engine: AsyncEngine, symbol: str, timeframe: str, limit: int = 100):
    query = text(
        """
        SELECT ts, open, high, low, close, volume
        FROM candles
        WHERE symbol = :symbol AND timeframe = :timeframe
        ORDER BY ts DESC
        LIMIT :limit
        """
    )
    async with engine.connect() as conn:
        rows = (await conn.execute(query, {"symbol": symbol, "timeframe": timeframe, "limit": limit})).all()
    return list(reversed(rows))

