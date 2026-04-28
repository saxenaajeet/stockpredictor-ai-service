from pydantic import BaseModel, Field
from typing import Literal


class RagQueryRequest(BaseModel):
    ticker: str = Field(
        ...,
        min_length=1,
        description="Stock ticker"
    )
    question: str = Field(
        ...,
        min_length=1,
        description="User query for RAG"
    )


class RagQueryResponse(BaseModel):
    question: str
    answer: str = Field(
        ...,
        description="Answer generated using RAG pipeline"
    )
    status: Literal["success", "error"] = Field(
        default="success",
        description="Response status"
    )