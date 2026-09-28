import httpx

from app.core.config import Settings


async def send_telegram_alert(settings: Settings, message: str) -> None:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(url, json={"chat_id": settings.telegram_chat_id, "text": message})

