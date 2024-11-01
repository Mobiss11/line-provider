# app/storage/redis.py
from typing import Dict, Optional
from app.models.events import Event
from redis import asyncio as aioredis
from app.core.config import settings


class RedisStorage:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)
        self.EVENT_PREFIX = "event:"

    async def store_event(self, event: Event) -> None:
        """Сохранение события в Redis"""
        event_key = f"{self.EVENT_PREFIX}{event.event_id}"
        await self.redis.set(event_key, event.model_dump_json())

    async def get_event(self, event_id: str) -> Optional[Event]:
        """Получение события по ID"""
        event_key = f"{self.EVENT_PREFIX}{event_id}"
        event_data = await self.redis.get(event_key)
        if event_data:
            return Event.model_validate_json(event_data)
        return None

    async def get_all_events(self) -> list[Event]:
        """Получение всех событий"""
        events = []
        # Используем keys вместо scan_iter для простоты
        keys = await self.redis.keys(f"{self.EVENT_PREFIX}*")

        for key in keys:
            event_data = await self.redis.get(key)
            if event_data:
                event = Event.model_validate_json(event_data)
                events.append(event)

        return events
