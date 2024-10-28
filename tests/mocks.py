# tests/mocks.py
class MockRedis:
    def __init__(self):
        self.data = {}
        self.callbacks = []

    async def set(self, key: str, value: str, ex: int = None) -> None:
        self.data[key] = value

    async def get(self, key: str) -> str:
        return self.data.get(key)

    async def flushdb(self) -> None:
        self.data.clear()
        self.callbacks.clear()

    async def scan_iter(self, match: str = None):
        # Возвращаем все ключи, соответствующие паттерну
        prefix = match.replace('*', '') if match else ''
        matching_keys = [k for k in self.data.keys() if k.startswith(prefix)]
        for key in matching_keys:
            yield key

    async def aclose(self) -> None:
        pass

    # Добавляем метод keys для альтернативной реализации
    async def keys(self, pattern: str = None) -> list:
        if pattern:
            prefix = pattern.replace('*', '')
            return [k for k in self.data.keys() if k.startswith(prefix)]
        return list(self.data.keys())