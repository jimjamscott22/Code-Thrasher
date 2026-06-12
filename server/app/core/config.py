from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "change-me-in-production-use-a-long-random-string"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "postgresql+asyncpg://codethrasher:codethrasher@localhost:5432/codethrasher"
    SECRET_KEY: str = DEFAULT_SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = "http://localhost:5173"

    # Sandbox limits
    SANDBOX_TIMEOUT_SECONDS: int = 5
    SANDBOX_MAX_MEMORY_MB: int = 64
    SANDBOX_MAX_OUTPUT_BYTES: int = 10_000

    @field_validator("CORS_ORIGINS")
    @classmethod
    def strip_cors_origins(cls, value: str) -> str:
        return value.strip()

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    def validate_production_settings(self) -> None:
        if self.ENVIRONMENT.lower() in {"production", "prod"} and self.SECRET_KEY == DEFAULT_SECRET_KEY:
            raise RuntimeError(
                "SECRET_KEY must be changed from the default placeholder in production"
            )


settings = Settings()
