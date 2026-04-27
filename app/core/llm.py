from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from app.config import settings


def get_llm(provider="openai"):
    if provider == "openai":
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=settings.openai_api_key
        )
    elif provider == "ollama":
        return ChatOllama(
            model="phi3",
            temperature=0.3
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")