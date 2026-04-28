# app/core/vector_store.py

from app.core.db import get_connection
from app.ingestion.embeddings import get_embedding_model
from app.config import settings

def store_documents(documents, ticker: str):

    conn = get_connection()
    cur = conn.cursor()

    # 🔥 STEP 1 — delete existing data for ticker
    cur.execute(
        "DELETE FROM stock_embeddings WHERE ticker = %s",
        (ticker,)
    )

    embedding_model = get_embedding_model(settings.embedding_provider)

    # 🔹 STEP 2 — insert fresh data
    for doc in documents:
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

    conn.commit()
    cur.close()
    conn.close()