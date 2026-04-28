# app/api/routes/rag_routes.py

from fastapi import APIRouter
from app.models.rag_models import RagQueryRequest, RagQueryResponse
from app.core.chains import run_rag_pipeline

router = APIRouter()


@router.post("/query", response_model=RagQueryResponse)
def query_rag(request: RagQueryRequest):

    answer = run_rag_pipeline(
        question=request.question,
        ticker=request.ticker
    )

    return RagQueryResponse(
        question=request.question,
        answer=answer,
        status="success"
    )