from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/chatdb"
    SECRET_KEY : str

    class Config:
        env_file = ".env"

settings = Settings()
