# app/core/vector_store.py

from app.core.db import get_connection
from app.ingestion.embeddings import get_embedding_model
from app.config import settings

def store_documents(documents, ticker: str):

    conn = get_connection()
    cur = conn.cursor()

    embedding_model = get_embedding_model(provider=settings.embedding_provider)

    for doc in documents:
        text = doc.page_content

        # 🔹 convert text → embedding
        embedding = embedding_model.embed_query(text)

        # 🔹 insert into DB
        cur.execute(
            """
            INSERT INTO stock_embeddings (ticker, content, embedding, source)
            VALUES (%s, %s, %s, %s)
            """,
            (
                ticker,
                text,
                embedding,   # list → stored as vector
                doc.metadata.get("source", "manual")
            )
        )

    conn.commit()
    cur.close()
    conn.close()