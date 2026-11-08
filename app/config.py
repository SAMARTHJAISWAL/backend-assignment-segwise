from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, read from environment variables or a local .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite:///./event_triggers.db"
    SECRET_API_KEY: str = "change-me"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    CACHE_ENABLED: bool = True
    CACHE_EXPIRATION: int = 3600
    # Event log retention: active for 2 hours, then archived, then deleted at 48 hours.
    ACTIVE_RETENTION_HOURS: int = 2
    TOTAL_RETENTION_HOURS: int = 48


settings = Settings()
