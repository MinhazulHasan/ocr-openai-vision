from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GPT_MODEL: str = "gpt-4o"
    ALLOWED_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
