from langchain_community.embeddings import OllamaEmbeddings, OpenAIEmbeddings
from app.config import settings


def get_embedding_model(provider="ollama"):

    if provider == "ollama":
        return OllamaEmbeddings(
            model=settings.embedding_model
        )

    elif provider == "openai":
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.openai_api_key
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")

def embed_documents(documents):
    embedding_model = get_embedding_model("ollama")
    texts = [doc.page_content for doc in documents]
    embeddings = embedding_model.embed_documents(texts)
    return embeddings