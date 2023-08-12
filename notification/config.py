from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MP3_QUEUE: str = "mp3"
    GMAIL_ADDRESS: str
    GMAIL_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
