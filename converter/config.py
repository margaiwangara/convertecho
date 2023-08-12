from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VIDEO_QUEUE: str = "video"
    MP3_QUEUE: str = "mp3"
    MONGO_URI: str

    class Config:
        env_file = ".env"


settings = Settings()
