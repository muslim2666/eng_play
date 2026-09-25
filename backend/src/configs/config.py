from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra_fields="ignore"
    )

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: str) -> str:
        if isinstance(v, str) and not v.startswith("postgresql+asyncpg://"):
            raise ValueError("Ссылка должна начинаться с postgresql+asyncpg://")
        return v

settings = Settings()
