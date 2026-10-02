from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_provider: str = "ollama"
    llm_model: str = "qwen3:8b"

    groq_api_key: str | None = None

    interests: str = "System Design,AI Engineering"

    email_sender: str | None = None
    email_password: str | None = None
    email_recipient: str | None = None

    scheduler_timezone: str = "Asia/Kolkata"
    daily_read_hour: int = 8
    daily_read_minute: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    def get_interests(self) -> list[str]:
        return [
            interest.strip()
            for interest in self.interests.split(",")
            if interest.strip()
        ]


settings = Settings()
