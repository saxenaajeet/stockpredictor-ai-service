from pydantic import BaseModel


class DocumentTestRequest(BaseModel):
    text: str
    source: str = "manual"


class DocumentTestResponse(BaseModel):
    source: str
    total_chunks: int
    chunks: list[str]

class DocumentSearchRequest(BaseModel):
    text: str
    question: str
    source: str = "manual"


class DocumentSearchResponse(BaseModel):
    question: str
    matched_chunks: list[str]
    total_matches: int
    status: str