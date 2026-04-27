from pydantic import BaseModel


class RagQueryRequest(BaseModel):
    question: str


class RagQueryResponse(BaseModel):
    question: str
    answer: str
    status: str