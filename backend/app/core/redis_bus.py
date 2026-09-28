import json
from collections.abc import AsyncIterator

from pydantic import BaseModel
from redis.asyncio import Redis

from app.core.config import get_settings


def get_redis() -> Redis:
    return Redis.from_url(get_settings().redis_url, decode_responses=True)


async def publish(channel: str, event: BaseModel) -> None:
    redis = get_redis()
    try:
        await redis.publish(channel, event.model_dump_json())
    finally:
        await redis.aclose()


async def subscribe(channel: str) -> AsyncIterator[dict]:
    redis = get_redis()
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                yield json.loads(message["data"])
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.aclose()
        await redis.aclose()

