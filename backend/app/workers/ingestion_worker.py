import asyncio
from datetime import UTC, datetime

from app.alerts.telegram import send_telegram_alert
from app.core.config import get_settings
from app.core.db import create_engine, insert_candle
from app.core.events import BusChannel, CandleEvent, HealthEvent
from app.core.redis_bus import publish


async def stream_placeholder():
    while True:
        yield CandleEvent(
            symbol="RELIANCE",
            timeframe="1m",
            ts=datetime.now(UTC),
            open=2840.0,
            high=2865.0,
            low=2838.0,
            close=2862.0,
            volume=125000,
        )
        await asyncio.sleep(60)


async def main() -> None:
    settings = get_settings()
    engine = create_engine()
    last_message = datetime.now(UTC)

    async for candle in stream_placeholder():
        await insert_candle(engine, candle)
        await publish(BusChannel.CANDLES, candle)
        last_message = datetime.now(UTC)

        if (datetime.now(UTC) - last_message).total_seconds() > 5:
            alert = "System Critical: broker WebSocket has been silent for more than 5 seconds."
            await send_telegram_alert(settings, alert)
            await publish(BusChannel.HEALTH, HealthEvent(component="data_feed", ok=False, message=alert))


if __name__ == "__main__":
    asyncio.run(main())

