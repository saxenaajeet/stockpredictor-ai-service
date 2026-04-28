import logging
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.ingestion.embeddings import get_embedding_model
from app.config import settings

logger = logging.getLogger(__name__)


def create_in_memory_vector_store(documents: List[Document]):
    """
    Creates an in-memory FAISS vector store.

    Flow:
    1. Validate documents
    2. Initialize embedding model
    3. Build FAISS index
    """

    try:
        if not documents:
            logger.warning("No documents provided for vector store creation")
            return None

        logger.info("Creating FAISS vector store with %d documents", len(documents))

        # Step 1: Initialize embedding model (correct config usage)
        embedding_model = get_embedding_model(settings.embedding_provider)

        # Step 2: Build FAISS index
        store = FAISS.from_documents(
            documents=documents,
            embedding=embedding_model
        )

        logger.info("FAISS vector store created successfully")

        return store

    except Exception:
        logger.error("Failed to create FAISS vector store", exc_info=True)
        raise


def search_similar_documents(
    documents: List[Document],
    query: str,
    k: int = 3
):
    """
    Performs similarity search over in-memory FAISS store.

    Flow:
    1. Validate input
    2. Create vector store
    3. Perform similarity search
    4. Return results
    """

    try:
        if not documents:
            logger.warning("No documents provided for search")
            return []

        if not query or not query.strip():
            logger.warning("Empty query received for similarity search")
            return []

        logger.info("Running similarity search, k=%d", k)

        # Step 1: Create vector store
        store = create_in_memory_vector_store(documents)

        if not store:
            logger.warning("Vector store creation failed or empty")
            return []

        # Step 2: Perform search
        results = store.similarity_search(query, k=k)

        logger.info("Similarity search completed, results=%d", len(results))

        return results

    except Exception:
        logger.error("Failed to perform similarity search", exc_info=True)
        raise