from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000
    database_url: str = "sqlite:///./data/rescuebridge.db"
    media_root: str = "./data/media"

    ai_mode: str = "local"
    local_model: str = "gemma4:e4b"
    ollama_base_url: str = "http://127.0.0.1:11434"
    allow_hosted_evaluation: bool = False
    ollama_timeout_seconds: float = 90.0
    gemini_api_key: str | None = None
    hosted_model: str = "gemma-4-26b-a4b-it"
    hosted_timeout_seconds: float = 90.0
    solana_cluster: str = "devnet"

    # The development script runs from backend/, while operators commonly keep
    # the real .env at repository root. Pydantic checks both locations.
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), env_prefix="", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
