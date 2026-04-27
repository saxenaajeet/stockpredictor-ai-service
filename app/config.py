from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "StockPredictor AI Service"
    app_version: str = "1.0.0"
    environment: str = "local"
    openai_api_key: str = "abcdef1234567890"
    provider: str = "ollama"
    embedding_provider: str = "nomic-embed-text"

    class Config:
        env_file = ".env"


settings = Settings()