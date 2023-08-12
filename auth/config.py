from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  MYSQL_HOST: str = "127.0.0.1"
  MYSQL_USER: str = "root"
  MYSQL_PASSWORD: str
  MYSQL_DB: str
  MYSQL_PORT: int
  JWT_SECRET: str
  
  class Config:
    env_file = ".env"
    
settings = Settings()