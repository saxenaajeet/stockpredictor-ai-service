import logging
from typing import List

from app.core.db import get_connection
from app.ingestion.embeddings import get_embedding_model
from app.config import settings

logger = logging.getLogger(__name__)


def search_similar_chunks(query: str, ticker: str, k: int = 3) -> List[str]:
    """
    Searches similar chunks from the vector database using pgvector.

    Flow:
    1. Validate input
    2. Generate query embedding
    3. Execute similarity search
    4. Return matched chunks
    """

    conn = None
    cur = None

    try:
        # Step 1: Validate input
        if not query or not query.strip():
            logger.warning("Empty query received for ticker=%s", ticker)
            return []

        if not ticker:
            logger.warning("Ticker is empty, skipping search")
            return []

        logger.info("Running similarity search for ticker=%s, k=%d", ticker, k)

        # Step 2: Create DB connection
        conn = get_connection()
        cur = conn.cursor()

        # Step 3: Generate embedding for query
        embedding_model = get_embedding_model(settings.embedding_provider)
        query_embedding = embedding_model.embed_query(query)

        logger.debug(
            "Generated query embedding for ticker=%s, dimension=%d",
            ticker,
            len(query_embedding)
        )

        # Step 4: Perform similarity search
        cur.execute(
            """
            SELECT content
            FROM stock_embeddings
            WHERE ticker = %s
            ORDER BY embedding <-> %s::vector
            LIMIT %s
            """,
            (ticker, query_embedding, k)
        )

        results = cur.fetchall()

        logger.info(
            "Similarity search completed for ticker=%s, results=%d",
            ticker,
            len(results)
        )

        return [r[0] for r in results]

    except Exception:
        logger.error(
            "Failed similarity search for ticker=%s",
            ticker,
            exc_info=True
        )
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()