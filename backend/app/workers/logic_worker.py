import asyncio

import pandas as pd

from app.core.db import create_engine, fetch_recent_candles
from app.core.events import BusChannel, CandleEvent, SignalEvent, SignalSide
from app.core.redis_bus import publish, subscribe
from app.services.indicator_engine import IndicatorEngine
from app.strategies import strategy_orb_plus


async def main() -> None:
    engine = create_engine()
    indicators = IndicatorEngine()

    async for payload in subscribe(BusChannel.CANDLES):
        candle = CandleEvent.model_validate(payload)
        rows = await fetch_recent_candles(engine, candle.symbol, candle.timeframe)
        df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
        df = df.set_index("ts")
        df = indicators.enrich(df)

        decision = strategy_orb_plus(df)
        if decision.side == SignalSide.WAIT:
            continue

        signal = SignalEvent(
            symbol=candle.symbol,
            strategy="orb_plus",
            side=decision.side,
            entry_price=float(df["close"].iloc[-1]),
            stop_loss=float(decision.stop_loss),
            target_price=decision.target_price,
            atr=float(df["atr"].iloc[-1]) if not pd.isna(df["atr"].iloc[-1]) else None,
            reason=decision.reason,
        )
        await publish(BusChannel.SIGNALS, signal)


if __name__ == "__main__":
    asyncio.run(main())

