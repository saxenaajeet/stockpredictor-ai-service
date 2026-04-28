import logging

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from app.config import settings

logger = logging.getLogger(__name__)


def get_llm(provider: str | None = None):
    """
    Factory to initialize LLM based on provider.

    Flow:
    1. Resolve provider (input > config)
    2. Validate config
    3. Return appropriate LLM instance
    """

    try:
        # Step 1: Resolve provider
        provider = (provider or settings.llm_provider).lower()
        logger.info("Initializing LLM with provider=%s", provider)

        # Step 2: OpenAI
        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is not configured")

            logger.info("Using OpenAI model=%s", settings.llm_model)

            return ChatOpenAI(
                model=settings.llm_model,
                temperature=0.3,
                api_key=settings.openai_api_key
            )

        # Step 3: Ollama
        elif provider == "ollama":
            logger.info("Using Ollama model=%s", settings.llm_model)

            return ChatOllama(
                model=settings.llm_model,
                temperature=0.3
            )

        # Step 4: Unsupported provider
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception:
        logger.error("Failed to initialize LLM", exc_info=True)
        raise