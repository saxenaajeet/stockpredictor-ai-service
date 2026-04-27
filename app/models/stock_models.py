from pydantic import BaseModel


class StockResearchRequest(BaseModel):
    ticker: str


class StockResearchResponse(BaseModel):
    ticker: str
    summary: str
    status: str