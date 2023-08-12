from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_VIDEOS_URI: str
    MONGO_MP3S_URI: str
    AUTH_SERVICE_ADDRESS: str

    class Config:
        env_file = ".env"


settings = Settings()
