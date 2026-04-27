from pydantic import BaseModel


class RagQueryRequest(BaseModel):
    text: str
    question: str
    source: str = "manual"


class RagQueryResponse(BaseModel):
    question: str
    answer: str
    status: str