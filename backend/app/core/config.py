from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    trading_mode: str = "paper"
    database_url: str = "postgresql+asyncpg://trader:trader@localhost:5432/trading"
    redis_url: str = "redis://localhost:6379/0"
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    broker_provider: str = "paper"
    max_daily_drawdown_pct: float = 2.0
    account_starting_capital: float = 1_000_000
    risk_per_trade_pct: float = 0.5
    dashboard_cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])


@lru_cache
def get_settings() -> Settings:
    return Settings()
