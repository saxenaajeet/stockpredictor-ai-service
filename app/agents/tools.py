

def rag_tool(ticker: str, question: str):
    from app.retrieval.search import search_similar_chunks

    results = search_similar_chunks(
        ticker=ticker,
        query=question,
        k=5
    )

    return "\n".join(results)


def yahoo_tool(ticker: str):
    from app.ingestion.yahoo_loader import fetch_stock_data

    return fetch_stock_data(ticker)