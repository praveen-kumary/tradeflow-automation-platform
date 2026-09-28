import pandas as pd

from app.core.events import SignalSide
from app.strategies.orb_plus import strategy_orb_plus


def test_orb_plus_buy_signal_on_confirmed_breakout():
    index = pd.date_range("2026-04-27 09:15", periods=25, freq="1min", tz="Asia/Kolkata")
    df = pd.DataFrame(
        {
            "open": [100] * 25,
            "high": [101] * 16 + [103] * 9,
            "low": [99] * 25,
            "close": [100] * 23 + [101, 103],
            "volume": [1000] * 25,
            "ema_20": [99] * 25,
            "rsi": [60] * 25,
            "atr": [2] * 25,
        },
        index=index,
    )

    decision = strategy_orb_plus(df)

    assert decision.side == SignalSide.BUY
    assert decision.stop_loss == 99
    assert "ORB Breakout" in decision.reason

