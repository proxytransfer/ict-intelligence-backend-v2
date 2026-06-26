from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    JWT_SECRET: str = "your_secret_here"
    CACHE_TTL: int = 300  # 5 minutes
    PROVIDER_RETRY_ATTEMPTS: int = 3
    CALIBRATION_K: float = 20.0
    CORS_ORIGINS: List[str] = ["https://*.lovable.app", "http://localhost:5173"]
    DATABASE_URL: str = "sqlite+aiosqlite:///./data.db"
    CACHE_DB_PATH: str = "/tmp/cache.db"
    WS_HEARTBEAT: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
