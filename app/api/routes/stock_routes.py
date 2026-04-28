import logging

from fastapi import APIRouter, HTTPException
from app.models.stock_models import (
    StockResearchRequest,
    StockResearchResponse
)
from app.core.chains import get_stock_research_chain

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/research", response_model=StockResearchResponse)
def research_stock(request: StockResearchRequest):
    """
    Stock research endpoint.

    Flow:
    1. Normalize ticker
    2. Build research chain
    3. Invoke LLM chain
    4. Return structured summary
    """

    try:
        ticker = request.ticker.upper()
        logger.info("Stock research request received for ticker=%s", ticker)

        # Step 1: Build chain
        logger.info("Initializing stock research chain")
        chain = get_stock_research_chain()

        # Step 2: Invoke chain
        logger.info("Invoking research chain for ticker=%s", ticker)
        result = chain.invoke({
            "ticker": ticker
        })

        if not result or not getattr(result, "content", None):
            logger.warning("Empty research response for ticker=%s", ticker)

            raise HTTPException(
                status_code=502,
                detail="Stock research chain returned empty response"
            )

        logger.info("Stock research completed successfully for ticker=%s", ticker)

        # Step 3: Return response
        return StockResearchResponse(
            ticker=ticker,
            summary=result.content,
            status="success"
        )

    except HTTPException:
        raise

    except Exception:
        logger.error(
            "Stock research failed for ticker=%s",
            ticker if 'ticker' in locals() else "unknown",
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing stock research"
        )