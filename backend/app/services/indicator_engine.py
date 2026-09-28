import pandas as pd

try:
    import pandas_ta as ta
except ImportError:  # pragma: no cover - keeps tests useful before deps are installed
    try:
        import pandas_ta_classic as ta
    except ImportError:
        ta = None


class IndicatorEngine:
    def enrich(self, candles: pd.DataFrame) -> pd.DataFrame:
        df = candles.copy()
        if ta is not None:
            df["ema_20"] = ta.ema(df["close"], length=20)
            df["rsi"] = ta.rsi(df["close"], length=14)
            df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
            return df

        df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()
        delta = df["close"].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / loss.replace(0, pd.NA)
        df["rsi"] = 100 - (100 / (1 + rs))
        ranges = pd.concat(
            [
                df["high"] - df["low"],
                (df["high"] - df["close"].shift()).abs(),
                (df["low"] - df["close"].shift()).abs(),
            ],
            axis=1,
        )
        df["atr"] = ranges.max(axis=1).rolling(14).mean()
        return df
