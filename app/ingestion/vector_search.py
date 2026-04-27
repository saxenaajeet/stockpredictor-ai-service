

from langchain_community.vectorstores import FAISS
from app.ingestion.embeddings import get_embedding_model
from app.ingestion import vector_store
from app.config import settings


def create_in_memory_vector_store(documents):
    embedding_model = get_embedding_model(provider=settings.provider)

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embedding_model
    )

    return vector_store


def search_similar_documents(documents, query: str, k: int = 3):
    vector_store = create_in_memory_vector_store(documents)
    results = vector_store.similarity_search(query, k=k)
    return results