import asyncio

from app.broker.paper import PaperBroker
from app.core.config import get_settings
from app.core.events import BusChannel, ExecutionEvent, SignalEvent
from app.core.redis_bus import publish, subscribe
from app.risk.risk_engine import RiskEngine


async def main() -> None:
    settings = get_settings()
    broker = PaperBroker()
    risk = RiskEngine(settings)

    async for payload in subscribe(BusChannel.SIGNALS):
        signal = SignalEvent.model_validate(payload)
        risk.evaluate_daily_mtm(await broker.current_mtm())
        decision = risk.size_order(signal)

        if not decision.allowed:
            await publish(
                BusChannel.EXECUTION,
                ExecutionEvent(symbol=signal.symbol, status="blocked", message=decision.reason),
            )
            continue

        order_id = await broker.place_order(signal, decision.quantity)
        await publish(
            BusChannel.EXECUTION,
            ExecutionEvent(
                symbol=signal.symbol,
                status="placed",
                message=f"{signal.side} {decision.quantity} via {signal.strategy}",
                order_id=order_id,
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

