import logging
from typing import List

from langchain_core.documents import Document

from app.core.db import get_connection
from app.ingestion.embeddings import get_embedding_model
from app.config import settings

logger = logging.getLogger(__name__)


def store_documents(documents: List[Document], ticker: str):
    """
    Stores documents and their embeddings in the database.

    Flow:
    1. Validate input
    2. Open DB connection
    3. Delete existing data for ticker
    4. Generate embeddings + insert
    5. Commit transaction
    """

    conn = None
    cur = None

    try:
        if not documents:
            logger.warning("No documents provided for storage, ticker=%s", ticker)
            return

        if not ticker:
            logger.warning("Ticker is empty, skipping storage")
            return

        logger.info("Storing %d documents for ticker=%s", len(documents), ticker)

        # Step 1: DB connection
        conn = get_connection()
        cur = conn.cursor()

        # Step 2: Delete existing data
        logger.info("Deleting existing embeddings for ticker=%s", ticker)
        cur.execute(
            "DELETE FROM stock_embeddings WHERE ticker = %s",
            (ticker,)
        )

        # Step 3: Initialize embedding model
        embedding_model = get_embedding_model(settings.embedding_provider)

        # Step 4: Insert new embeddings
        inserted_count = 0

        for doc in documents:
            if not doc.page_content:
                continue

            embedding = embedding_model.embed_query(doc.page_content)

            cur.execute(
                """
                INSERT INTO stock_embeddings (ticker, content, embedding, source)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    ticker,
                    doc.page_content,
                    embedding,
                    doc.metadata.get("source", "manual")
                )
            )

            inserted_count += 1

        # Step 5: Commit transaction
        conn.commit()

        logger.info(
            "Successfully stored %d documents for ticker=%s",
            inserted_count,
            ticker
        )

    except Exception:
        if conn:
            conn.rollback()

        logger.error(
            "Failed to store documents for ticker=%s",
            ticker,
            exc_info=True
        )
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()