from app.core.db import get_connection
from app.ingestion.embeddings import get_embedding_model
from app.config import settings


def search_similar_chunks(query: str, ticker: str, k: int = 3):

    conn = get_connection()
    cur = conn.cursor()

    embedding_model = get_embedding_model(settings.embedding_provider)

    query_embedding = embedding_model.embed_query(query)

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

    cur.close()
    conn.close()

    return [r[0] for r in results]