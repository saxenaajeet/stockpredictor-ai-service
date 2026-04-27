# app/api/routes/llm_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.core.llm import get_llm
from app.models.llm_models import AskRequest, AskResponse

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_phi3(request: AskRequest):
    llm = get_llm(provider="ollama")
    result = llm.invoke(request.question)
    return AskResponse(answer=result.content)