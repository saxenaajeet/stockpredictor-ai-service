from pydantic import BaseModel


class RagQueryRequest(BaseModel):
    ticker: str
    question: str
    

class RagQueryResponse(BaseModel):
    question: str
    answer: str
    status: str