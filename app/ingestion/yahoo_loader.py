import yfinance as yf


def fetch_stock_data(ticker: str) -> str:
    stock = yf.Ticker(ticker)

    info = stock.info
    news = stock.news if hasattr(stock, "news") else []

    text_parts = []

    # Basic company info
    if info:
        text_parts.append(f"Company: {info.get('longName', '')}")
        text_parts.append(f"Sector: {info.get('sector', '')}")
        text_parts.append(f"Industry: {info.get('industry', '')}")
        text_parts.append(f"Summary: {info.get('longBusinessSummary', '')}")

    # News
    for article in news[:5]:
        text_parts.append(article.get("title", ""))
        text_parts.append(article.get("summary", ""))

    return "\n".join(text_parts)