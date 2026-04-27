from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "StockPredictor AI Service"
    app_version: str = "1.0.0"
    environment: str = "local"
    openai_api_key: str = "abcdef1234567890"

    class Config:
        env_file = ".env"


settings = Settings()