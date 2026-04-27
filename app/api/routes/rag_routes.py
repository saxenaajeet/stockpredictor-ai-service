# app/api/routes/rag_routes.py

from fastapi import APIRouter
from app.models.rag_models import RagQueryRequest, RagQueryResponse
from app.core.chains import get_rag_query_chain

router = APIRouter()


@router.post("/query", response_model=RagQueryResponse)
def query_rag(request: RagQueryRequest):
    chain = get_rag_query_chain()

    result = chain.invoke({
        "question": request.question
    })

    return RagQueryResponse(
        question=request.question,
        answer=result.content,
        status="success"
    )