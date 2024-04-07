from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    tg_token: str = Field(..., alias='TELEGRAM_TOKEN')
    kp_token: str = Field(..., alias='KP_TOKEN')
    kinoclub_token: str = Field(..., alias='KINOCLUB_TOKEN')
    chat_url: str = Field(..., alias='CHAT_URL')
    chat_id: str = Field(..., alias='CHAT_ID')


settings = Settings()
