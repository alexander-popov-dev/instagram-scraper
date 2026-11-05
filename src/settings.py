from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    debug: bool = False
    headless: bool = False if debug else True

    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    telegram_thread_id: str = ""

    if debug:
        headless = False


@cache
def get_settings() -> BaseProjectSettings:
    return BaseProjectSettings()
