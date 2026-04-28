from pydantic import BaseModel


class DocumentTestRequest(BaseModel):
    source: str


class DocumentTestResponse(BaseModel):
    source: str
    total_chunks: int
    chunks: list[str]

class DocumentSearchRequest(BaseModel):
    ticker: str
    question: str


class DocumentSearchResponse(BaseModel):
    question: str
    matched_chunks: list[str]
    total_matches: int
    status: str