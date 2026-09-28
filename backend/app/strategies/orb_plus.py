import pandas as pd

from app.core.events import SignalSide
from app.strategies.base import StrategyDecision


def strategy_orb_plus(df: pd.DataFrame) -> StrategyDecision:
    """Enhanced Opening Range Breakout with RSI and EMA confirmation."""
    if len(df) < 21:
        return StrategyDecision(SignalSide.WAIT, None, None, "Need at least 21 candles")

    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("strategy_orb_plus requires a DatetimeIndex")

    morning_range = df.between_time("09:15", "09:30", inclusive="both")
    if morning_range.empty:
        return StrategyDecision(SignalSide.WAIT, None, None, "Opening range not available")

    orb_high = float(morning_range["high"].max())
    orb_low = float(morning_range["low"].min())
    current = df.iloc[-1]
    previous = df.iloc[-2]

    if pd.isna(current.get("ema_20")) or pd.isna(current.get("rsi")):
        return StrategyDecision(SignalSide.WAIT, None, None, "Indicators warming up")

    crossed_orb = previous["close"] <= orb_high < current["close"]
    trend_confirmed = current["rsi"] > 55 and current["close"] > current["ema_20"]

    if crossed_orb and trend_confirmed:
        risk = current["close"] - orb_low
        target = current["close"] + (risk * 2)
        return StrategyDecision(
            SignalSide.BUY,
            orb_low,
            float(target),
            "ORB Breakout + RSI > 55 + EMA20 confirmation",
        )

    return StrategyDecision(SignalSide.WAIT, None, None, "No ORB confirmation")

