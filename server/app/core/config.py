from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "postgresql+asyncpg://codethrasher:codethrasher@localhost:5432/codethrasher"
    SECRET_KEY: str = "change-me-in-production-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Sandbox limits
    SANDBOX_TIMEOUT_SECONDS: int = 5
    SANDBOX_MAX_MEMORY_MB: int = 64
    SANDBOX_MAX_OUTPUT_BYTES: int = 10_000


settings = Settings()
