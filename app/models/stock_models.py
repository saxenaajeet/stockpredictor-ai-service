from pydantic import BaseModel, Field
from typing import Literal


class StockResearchRequest(BaseModel):
    ticker: str = Field(
        ...,
        min_length=1,
        description="Stock ticker symbol"
    )


class StockResearchResponse(BaseModel):
    ticker: str
    summary: str = Field(
        ...,
        description="Generated stock research summary"
    )
    status: Literal["success", "error"] = Field(
        default="success",
        description="Response status"
    )