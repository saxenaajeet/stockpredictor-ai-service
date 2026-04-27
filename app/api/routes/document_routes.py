from fastapi import APIRouter
from app.models.document_models import *
from app.ingestion.document_loader import load_text_as_document
from app.ingestion.text_splitter import split_documents
from app.ingestion.vector_search import search_similar_documents

router = APIRouter()


@router.post("/split", response_model=DocumentTestResponse)
def split_text(request: DocumentTestRequest):
    documents = load_text_as_document(
        text=request.text,
        source=request.source
    )

    chunks = split_documents(documents)

    return DocumentTestResponse(
        source=request.source,
        total_chunks=len(chunks),
        chunks=[chunk.page_content for chunk in chunks]
    )

@router.post("/search", response_model=DocumentSearchResponse)
def search_documents(request: DocumentSearchRequest):
    documents = load_text_as_document(
        text=request.text,
        source=request.source
    )

    chunks = split_documents(documents)

    matched_docs = search_similar_documents(
        documents=chunks,
        query=request.question,
        k=3
    )

    return DocumentSearchResponse(
        question=request.question,
        matched_chunks=[doc.page_content for doc in matched_docs],
        total_matches=len(matched_docs),
        status="success"
    )