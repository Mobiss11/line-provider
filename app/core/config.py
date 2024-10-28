from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Line Provider Service"
    DEBUG: bool = False
    REDIS_URL: str = "redis://redis:6379/0"
    EVENT_EXTRA_TTL: int = 60 * 60 * 24 * 7  # 7 дней
    CALLBACK_TTL: int = 60 * 60 * 24  # 24 часа

    class Config:
        env_file = ".env"


settings = Settings()
