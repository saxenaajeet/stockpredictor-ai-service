from fastapi import APIRouter
from app.models.document_models import *
from app.ingestion.document_loader import load_text_as_document
from app.ingestion.text_splitter import split_documents
from app.ingestion.vector_store import store_documents
from app.retrieval.search import search_similar_chunks
from app.ingestion.yahoo_loader import fetch_stock_data

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

    matched_chunks = search_similar_chunks(
        query=request.question,
        ticker=request.ticker,
        k=3
    )

    return DocumentSearchResponse(
        question=request.question,
        matched_chunks=matched_chunks,
        total_matches=len(matched_chunks),
        status="success"
    )

@router.post("/load")
def load_documents(request: DocumentTestRequest):

     # 🔹 Step 1: fetch data from Yahoo
    raw_text = fetch_stock_data(request.source)

    documents = load_text_as_document(
        text=raw_text,
        source=request.source
    )

    chunks = split_documents(documents)

    store_documents(chunks, ticker=request.source)

    return {
        "message": "Documents stored successfully",
        "chunks": len(chunks)
    }