from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question to be sent to the LLM"
    )


class AskResponse(BaseModel):
    answer: str = Field(
        ...,
        description="LLM generated answer"
    )
    status: str = Field(
        default="success",
        description="Response status"
    )