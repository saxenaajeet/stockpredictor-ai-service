import logging

from langchain_community.embeddings import OllamaEmbeddings, OpenAIEmbeddings

from app.config import settings

logger = logging.getLogger(__name__)


def get_embedding_model(provider: str | None = None):
    """
    Factory to initialize embedding model.

    Flow:
    1. Resolve provider (input > config)
    2. Validate config
    3. Return embedding model instance
    """

    try:
        provider = (provider or settings.embedding_provider).lower()
        logger.info("Initializing embedding model with provider=%s", provider)

        if provider == "ollama":
            logger.info("Using Ollama embedding model=%s", settings.embedding_model)

            return OllamaEmbeddings(
                model=settings.embedding_model
            )

        elif provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is not configured")

            logger.info("Using OpenAI embedding model=%s", settings.embedding_model)

            return OpenAIEmbeddings(
                model=settings.embedding_model,
                api_key=settings.openai_api_key
            )

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception:
        logger.error("Failed to initialize embedding model", exc_info=True)
        raise


def embed_documents(documents, provider: str | None = None):
    """
    Generate embeddings for a list of documents.

    Flow:
    1. Validate documents
    2. Extract text
    3. Generate embeddings
    """

    try:
        if not documents:
            logger.warning("No documents provided for embedding")
            return []

        logger.info("Embedding %d documents", len(documents))

        # Step 1: Initialize embedding model
        embedding_model = get_embedding_model(provider)

        # Step 2: Extract text content
        texts = [doc.page_content for doc in documents if doc.page_content]

        if not texts:
            logger.warning("No valid text found in documents")
            return []

        logger.debug("Total text items for embedding=%d", len(texts))

        # Step 3: Generate embeddings
        embeddings = embedding_model.embed_documents(texts)

        logger.info("Embeddings generated successfully, count=%d", len(embeddings))

        return embeddings

    except Exception:
        logger.error("Failed to generate embeddings", exc_info=True)
        raise