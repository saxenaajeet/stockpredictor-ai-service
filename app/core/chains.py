import logging

from app.core.llm import get_llm
from app.core.prompts import stock_research_prompt, rag_query_prompt
from app.config import settings
from app.retrieval.search import search_similar_chunks

logger = logging.getLogger(__name__)


def get_stock_research_chain():
    """
    Creates the stock research chain.
    """

    logger.info("Creating stock research chain with provider=%s", settings.embedding_provider)

    llm = get_llm(provider=settings.embedding_provider)
    return stock_research_prompt | llm


def get_rag_query_chain():
    """
    Creates the RAG query chain.
    """

    logger.info("Creating RAG query chain with provider=%s", settings.embedding_provider)

    llm = get_llm(provider=settings.embedding_provider)
    return rag_query_prompt | llm


def run_rag_pipeline(question: str, ticker: str):
    """
    Runs the full RAG pipeline.

    Flow:
    1. Search similar chunks
    2. Build context
    3. Invoke RAG chain
    4. Return answer
    """

    try:
        logger.info("Starting RAG pipeline for ticker=%s", ticker)

        # Step 1: Retrieve relevant chunks from vector store
        matched_chunks = search_similar_chunks(
            query=question,
            ticker=ticker,
            k=5
        )

        if not matched_chunks:
            logger.warning("No matching chunks found for ticker=%s", ticker)
            return "No relevant context found for this ticker."

        logger.debug(
            "Retrieved %d chunks for ticker=%s",
            len(matched_chunks),
            ticker
        )

        # Step 2: Join retrieved chunks into context
        context = "\n\n".join(matched_chunks)

        # Avoid printing full context in production
        logger.debug(
            "Built RAG context for ticker=%s, context_length=%d",
            ticker,
            len(context)
        )

        # Step 3: Create RAG chain
        chain = get_rag_query_chain()

        # Step 4: Invoke chain with question and context
        logger.info("Invoking RAG chain for ticker=%s", ticker)

        result = chain.invoke({
            "question": question,
            "context": context
        })

        if not result or not getattr(result, "content", None):
            logger.warning("RAG chain returned empty response for ticker=%s", ticker)
            return "Unable to generate an answer from the retrieved context."

        logger.info("RAG pipeline completed successfully for ticker=%s", ticker)

        return result.content

    except Exception:
        logger.error("RAG pipeline failed for ticker=%s", ticker, exc_info=True)
        raise