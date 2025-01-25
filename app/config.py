from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./event_triggers.db"
    CACHE_EXPIRATION: int = 3600  

settings = Settings()
