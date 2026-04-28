from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from environment variables or .env file.
    """

    # --- App ---
    app_name: str = "StockPredictor AI Service"
    app_version: str = "1.0.0"
    environment: str = "local"  # local / dev / prod

    # --- Logging ---
    logging_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR

    # --- LLM ---
    llm_provider: str = "ollama"   # openai / ollama
    llm_model: str = "phi3"

    openai_api_key: str | None = None  # should come from .env

    # --- Embeddings ---
    embedding_provider: str = "ollama"
    embedding_model: str = "nomic-embed-text"

    # --- Database ---
    db_name: str = "stock_ai"
    db_user: str = "stockuser"
    db_password: str = "stockpass"
    db_host: str = "localhost"
    db_port: int = 5432

    # --- Pydantic config ---
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Singleton settings object
settings = Settings()