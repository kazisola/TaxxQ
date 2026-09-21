from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    app_name = "TaxxQ AI"
    description = "Ask your tax queries to Uncle Sam!"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    groq_api_key: SecretStr

settings = Settings() # type: ignore