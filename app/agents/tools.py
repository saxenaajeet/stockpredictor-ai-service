import logging

# Module-level logger
logger = logging.getLogger(__name__)


def rag_tool(ticker: str, question: str):
    """
    RAG Tool:
    Fetches top-k similar chunks for a given ticker + question.

    Flow:
    1. Perform semantic search
    2. Validate results
    3. Return combined context
    """

    try:
        logger.info("RAG tool started for ticker=%s", ticker)

        # Import inside function to avoid circular dependencies
        from app.retrieval.search import search_similar_chunks

        # Step 1: Perform semantic search
        results = search_similar_chunks(
            ticker=ticker,
            query=question,
            k=5
        )

        # Step 2: Validate results
        if not results:
            logger.warning("No RAG results found for ticker=%s", ticker)
            return "No relevant documents found."

        logger.debug("RAG results count=%d for ticker=%s", len(results), ticker)

        # Step 3: Combine results
        combined = "\n".join(results)

        logger.info("RAG tool completed successfully for ticker=%s", ticker)
        return combined

    except Exception:
        logger.error("Error in RAG tool for ticker=%s", ticker, exc_info=True)
        return "Error retrieving contextual data."


def yahoo_tool(ticker: str):
    """
    Yahoo Finance Tool:
    Fetches stock-related data for a given ticker.

    Flow:
    1. Fetch stock data
    2. Validate response
    3. Return structured data
    """

    try:
        logger.info("Yahoo tool started for ticker=%s", ticker)

        # Import inside function to keep tools decoupled
        from app.ingestion.yahoo_loader import fetch_stock_data

        # Step 1: Fetch stock data
        data = fetch_stock_data(ticker)

        # Step 2: Validate response
        if not data:
            logger.warning("No Yahoo data found for ticker=%s", ticker)
            return "No stock data available."

        # Avoid logging full payload (can be large)
        logger.debug("Yahoo data fetched successfully for ticker=%s", ticker)

        logger.info("Yahoo tool completed successfully for ticker=%s", ticker)
        return data

    except Exception:
        logger.error("Error in Yahoo tool for ticker=%s", ticker, exc_info=True)
        return "Error fetching stock data."