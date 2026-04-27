from pydantic import BaseModel


class DocumentTestRequest(BaseModel):
    text: str
    source: str = "manual"


class DocumentTestResponse(BaseModel):
    source: str
    total_chunks: int
    chunks: list[str]