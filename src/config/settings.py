from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    host: str = Field(alias="HOST")
    port: int = Field(alias="PORT")

    database_url: str = Field(alias="DATABASE_URL")
    database_uri: str = Field(alias="DATABASE_URI")

    groq_model: str = Field(alias="GROQ_MODEL")
    groq_api_key: SecretStr = Field(alias="GROQ_API_KEY")
    jev_api_key: str = Field(alias="JEV_API_KEY")

    max_iterations: int = Field(default=3)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
