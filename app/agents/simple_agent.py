import logging

from app.core.llm import get_llm
from app.config import settings
from app.agents.tools import rag_tool, yahoo_tool
from app.core.prompts import agent_prompt

# Logging level/config should be controlled centrally from config.py
logger = logging.getLogger(__name__)


def run_agent(question: str, ticker: str):
    """
    Main agent execution function.

    Flow:
    1. Initialize LLM
    2. Fetch data from tools
    3. Build prompt + LLM chain
    4. Invoke chain with combined context
    5. Return final response
    """

    try:
        logger.info("Starting agent execution")
        logger.info("Input received for ticker=%s", ticker)

        # Step 1: Initialize LLM based on configured provider
        logger.info("Initializing LLM with provider=%s", settings.embedding_provider)
        llm = get_llm(settings.embedding_provider)
        logger.info("LLM initialized successfully")

        # Step 2: Fetch contextual data from RAG
        logger.info("Calling RAG tool for ticker=%s", ticker)
        rag_data = rag_tool(ticker, question)

        if rag_data:
            logger.debug("RAG data fetched successfully")
        else:
            logger.warning("No RAG data returned for ticker=%s", ticker)

        # Step 3: Fetch stock data from Yahoo Finance
        logger.info("Calling Yahoo Finance tool for ticker=%s", ticker)
        yahoo_data = yahoo_tool(ticker)

        if yahoo_data:
            logger.debug("Yahoo Finance data fetched successfully")
        else:
            logger.warning("No Yahoo Finance data returned for ticker=%s", ticker)

        # Step 4: Create chain by combining prompt template with LLM
        logger.info("Building agent chain")
        chain = agent_prompt | llm

        # Step 5: Invoke LLM with combined context
        logger.info("Invoking LLM for ticker=%s", ticker)
        response = chain.invoke({
            "rag_data": rag_data,
            "yahoo_data": yahoo_data,
            "question": question
        })

        logger.info("Agent execution completed successfully for ticker=%s", ticker)

        return response.content

    except Exception as e:
        logger.error("Agent execution failed for ticker=%s", ticker, exc_info=True)
        raise RuntimeError(f"Agent execution failed: {str(e)}")