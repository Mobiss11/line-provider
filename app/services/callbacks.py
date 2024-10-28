import json
from datetime import datetime, timedelta

import httpx

from app.storage.redis import RedisStorage
from app.core.config import settings


class CallbackService:
    def __init__(self, storage: RedisStorage):
        self.storage = storage
        self.callback_key = 'callbacks'
        self.ping_timeout = 5  # таймаут для пинга в секундах

    async def register_callback(self, callback_url: str) -> None:
        """Регистрация нового callback URL"""
        # Проверяем доступность URL перед регистрацией
        if await self._ping_callback(callback_url):
            callbacks = await self.get_callbacks()
            callbacks[callback_url] = {
                "url": callback_url,
                "last_active": datetime.now().isoformat(),
                "status": "active"
            }
            await self.storage.redis.set(
                self.callback_key,
                json.dumps(callbacks),
                ex=settings.CALLBACK_TTL
            )
        else:
            raise ValueError(f"Callback URL {callback_url} недоступен")

    async def get_callbacks(self) -> dict:
        """Получение списка активных callbacks"""
        callbacks_data = await self.storage.redis.get(self.callback_key)
        return json.loads(callbacks_data) if callbacks_data else {}

    async def update_callback_activity(self, callback_url: str) -> None:
        """Обновление времени последней активности"""
        callbacks = await self.get_callbacks()
        if callback_url in callbacks:
            callbacks[callback_url].update({
                "last_active": datetime.now().isoformat(),
                "status": "active"
            })
            await self.storage.redis.set(
                self.callback_key,
                json.dumps(callbacks),
                ex=settings.CALLBACK_TTL
            )

    async def _ping_callback(self, callback_url: str) -> bool:
        """Проверка доступности callback URL"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.head(
                    callback_url,
                    timeout=self.ping_timeout
                )
            return response.status_code < 500
        except Exception:
            return False

    async def check_callbacks_health(self) -> dict:
        """Проверка здоровья всех callbacks"""
        callbacks = await self.get_callbacks()
        results = {}

        for url, data in callbacks.items():
            last_active = datetime.fromisoformat(data["last_active"])
            is_active = await self._ping_callback(url)

            if not is_active:
                data["status"] = "inactive"
            elif datetime.now() - last_active > timedelta(seconds=settings.CALLBACK_TTL):
                data["status"] = "expired"
            else:
                data["status"] = "active"

            results[url] = data

        # Обновляем статусы в Redis
        await self.storage.redis.set(
            self.callback_key,
            json.dumps(results),
            ex=settings.CALLBACK_TTL
        )

        return results

    async def remove_inactive_callbacks(self) -> list:
        """Удаление неактивных callbacks"""
        callbacks = await self.get_callbacks()
        to_remove = []

        for url, data in callbacks.items():
            last_active = datetime.fromisoformat(data["last_active"])
            if (datetime.now() - last_active > timedelta(seconds=settings.CALLBACK_TTL) or
                    not await self._ping_callback(url)):
                to_remove.append(url)

        if to_remove:
            for url in to_remove:
                callbacks.pop(url, None)
            await self.storage.redis.set(
                self.callback_key,
                json.dumps(callbacks),
                ex=settings.CALLBACK_TTL
            )

        return to_remove
