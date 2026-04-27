from fastapi import APIRouter
from app.models.stock_models import StockResearchRequest, StockResearchResponse
from app.core.chains import get_stock_research_chain

router = APIRouter()


@router.post("/research", response_model=StockResearchResponse)
def research_stock(request: StockResearchRequest):
    ticker = request.ticker.upper()

    chain = get_stock_research_chain()
    result = chain.invoke({
        "ticker": ticker
    })

    return StockResearchResponse(
        ticker=ticker,
        summary=result.content,
        status="success"
    )