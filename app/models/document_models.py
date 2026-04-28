from pydantic import BaseModel, Field


class DocumentTestRequest(BaseModel):
    source: str = Field(..., min_length=1, description="Data source or ticker")


class DocumentTestResponse(BaseModel):
    source: str
    total_chunks: int = Field(..., ge=0)
    chunks: list[str] = Field(default_factory=list)


class DocumentSearchRequest(BaseModel):
    ticker: str = Field(..., min_length=1, description="Stock ticker")
    question: str = Field(..., min_length=1, description="User query")


class DocumentSearchResponse(BaseModel):
    question: str
    matched_chunks: list[str] = Field(default_factory=list)
    total_matches: int = Field(..., ge=0)
    status: str = Field(default="success")