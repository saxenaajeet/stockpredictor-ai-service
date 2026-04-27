# app/api/routes/rag_routes.py

from fastapi import APIRouter
from app.models.rag_models import RagQueryRequest, RagQueryResponse
from app.ingestion.document_loader import load_text_as_document
from app.ingestion.text_splitter import split_documents
from app.core.chains import run_rag_pipeline

router = APIRouter()


@router.post("/query", response_model=RagQueryResponse)
def query_rag(request: RagQueryRequest):
    documents = load_text_as_document(
        text=request.text,
        source=request.source
    )
    chunks = split_documents(documents)
    answer = run_rag_pipeline(
        question=request.question,
        documents=chunks
    )

    return RagQueryResponse(
        question=request.question,
        answer=answer,
        status="success"
    )