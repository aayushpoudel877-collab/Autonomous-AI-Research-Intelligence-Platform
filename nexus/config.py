from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "NEXUS Research Intelligence Platform"
    environment: str = "development"
    database_url: str = "sqlite:///./nexus.db"
    embedding_dimension: int = 256
    top_k: int = 5
    max_document_chars: int = 200_000
    model_config = SettingsConfigDict(env_prefix="NEXUS_", env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
