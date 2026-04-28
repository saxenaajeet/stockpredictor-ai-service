import logging
import yfinance as yf

logger = logging.getLogger(__name__)


def fetch_stock_data(ticker: str) -> str:
    """
    Fetches stock data and recent news from Yahoo Finance.

    Flow:
    1. Validate ticker
    2. Fetch stock info
    3. Extract company + news data
    4. Return combined text
    """

    try:
        if not ticker or not ticker.strip():
            logger.warning("Empty ticker received for Yahoo fetch")
            return ""

        ticker = ticker.upper()
        logger.info("Fetching stock data for ticker=%s", ticker)

        stock = yf.Ticker(ticker)

        # Step 1: Fetch data
        info = {}
        news = []

        try:
            info = stock.info or {}
        except Exception:
            logger.warning("Failed to fetch stock info for ticker=%s", ticker)

        try:
            news = stock.news if hasattr(stock, "news") else []
        except Exception:
            logger.warning("Failed to fetch news for ticker=%s", ticker)

        text_parts = []

        # Step 2: Basic company info
        if info:
            text_parts.append(f"Company: {info.get('longName', '')}")
            text_parts.append(f"Sector: {info.get('sector', '')}")
            text_parts.append(f"Industry: {info.get('industry', '')}")
            text_parts.append(f"Summary: {info.get('longBusinessSummary', '')}")

        else:
            logger.warning("No company info found for ticker=%s", ticker)

        # Step 3: News extraction
        if news:
            for article in news[:5]:
                title = article.get("title", "")
                summary = article.get("summary", "")

                if title:
                    text_parts.append(f"News Title: {title}")
                if summary:
                    text_parts.append(f"News Summary: {summary}")
        else:
            logger.warning("No news found for ticker=%s", ticker)

        result = "\n".join([part for part in text_parts if part])

        logger.info(
            "Fetched stock data for ticker=%s, length=%d",
            ticker,
            len(result)
        )

        return result

    except Exception:
        logger.error("Failed to fetch stock data for ticker=%s", ticker, exc_info=True)
        return ""