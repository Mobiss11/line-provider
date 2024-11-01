from typing import Optional, List, Dict
from datetime import datetime

from app.storage.redis import RedisStorage
from app.models.events import Event, EventStatus


class EventService:
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Конвертация строки в datetime"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError as e:
            raise ValueError(
                f"Неверный формат даты. Используйте формат: YYYY-MM-DDTHH:MM:SS, пример: 2024-03-25T12:00:00. Ошибка: {str(e)}")

    @staticmethod
    def _format_date(dt: datetime) -> str:
        """Конвертация datetime в строку"""
        return dt.strftime("%Y-%m-%dT%H:%M:%S")

    async def create_event(self, event: Event) -> Event:
        # Сохраняем ивент без модификаций, так как дата уже в строковом формате
        await self.storage.store_event(event)
        return event

    async def get_event(self, event_id: str) -> Optional[Event]:
        return await self.storage.get_event(event_id)

    async def get_all_events(self) -> list[Event]:
        return await self.storage.get_all_events()

    async def update_event_status(self, event_id: str, status: EventStatus) -> Optional[Event]:
        event = await self.get_event(event_id)
        if event:
            event.status = status
            await self.storage.store_event(event)
            return event
        return None
