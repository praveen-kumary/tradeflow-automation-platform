CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS candles (
  symbol TEXT NOT NULL,
  timeframe TEXT NOT NULL,
  ts TIMESTAMPTZ NOT NULL,
  open DOUBLE PRECISION NOT NULL,
  high DOUBLE PRECISION NOT NULL,
  low DOUBLE PRECISION NOT NULL,
  close DOUBLE PRECISION NOT NULL,
  volume BIGINT NOT NULL,
  PRIMARY KEY (symbol, timeframe, ts)
);

SELECT create_hypertable('candles', 'ts', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_candles_symbol_timeframe_ts
  ON candles (symbol, timeframe, ts DESC);

CREATE TABLE IF NOT EXISTS trade_events (
  id BIGSERIAL PRIMARY KEY,
  ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  event_type TEXT NOT NULL,
  symbol TEXT,
  payload JSONB NOT NULL DEFAULT '{}'::jsonb
);

