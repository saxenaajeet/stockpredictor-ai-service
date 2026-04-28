import logging
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.config import settings

logger = logging.getLogger(__name__)


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Splits documents into smaller chunks for embedding.

    Flow:
    1. Validate input documents
    2. Initialize text splitter (config-driven)
    3. Split into chunks
    4. Return chunked documents
    """

    try:
        if not documents:
            logger.warning("No documents provided for splitting")
            return []

        logger.info("Splitting %d documents", len(documents))

        # Step 1: Initialize splitter (use config if available)
        chunk_size = getattr(settings, "chunk_size", 300)
        chunk_overlap = getattr(settings, "chunk_overlap", 100)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        logger.debug(
            "Text splitter config: chunk_size=%d, chunk_overlap=%d",
            chunk_size,
            chunk_overlap
        )

        # Step 2: Split documents
        chunks = splitter.split_documents(documents)

        if not chunks:
            logger.warning("No chunks generated after splitting")
            return []

        logger.info("Generated %d chunks", len(chunks))

        return chunks

    except Exception:
        logger.error("Failed to split documents", exc_info=True)
        raise