import logging

from fastapi import APIRouter, HTTPException

from app.models.document_models import (
    DocumentTestRequest,
    DocumentTestResponse,
    DocumentSearchRequest,
    DocumentSearchResponse,
)
from app.ingestion.document_loader import load_text_as_document
from app.ingestion.text_splitter import split_documents
from app.ingestion.vector_store import store_documents
from app.retrieval.search import search_similar_chunks
from app.ingestion.yahoo_loader import fetch_stock_data

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/split", response_model=DocumentTestResponse)
def split_text(request: DocumentTestRequest):
    """
    Splits raw text into smaller document chunks.
    """

    try:
        logger.info("Split request received for source=%s", request.source)

        # Step 1: Convert raw text into LangChain document format
        documents = load_text_as_document(
            text=request.text,
            source=request.source
        )

        # Step 2: Split documents into chunks
        chunks = split_documents(documents)

        logger.info(
            "Text split completed for source=%s, total_chunks=%d",
            request.source,
            len(chunks)
        )

        # Step 3: Return chunks
        return DocumentTestResponse(
            source=request.source,
            total_chunks=len(chunks),
            chunks=[chunk.page_content for chunk in chunks]
        )

    except Exception:
        logger.error(
            "Failed to split text for source=%s",
            request.source,
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to split document text"
        )


@router.post("/search", response_model=DocumentSearchResponse)
def search_documents(request: DocumentSearchRequest):
    """
    Searches similar document chunks using ticker and question.
    """

    try:
        logger.info("Search request received for ticker=%s", request.ticker)

        # Step 1: Search top matching chunks from vector store
        matched_chunks = search_similar_chunks(
            query=request.question,
            ticker=request.ticker,
            k=3
        )

        logger.info(
            "Search completed for ticker=%s, total_matches=%d",
            request.ticker,
            len(matched_chunks)
        )

        # Step 2: Return matched chunks
        return DocumentSearchResponse(
            question=request.question,
            matched_chunks=matched_chunks,
            total_matches=len(matched_chunks),
            status="success"
        )

    except Exception:
        logger.error(
            "Failed to search documents for ticker=%s",
            request.ticker,
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to search documents"
        )


@router.post("/load")
def load_documents(request: DocumentTestRequest):
    """
    Loads stock data, splits it into chunks, and stores it in the vector store.
    """

    try:
        logger.info("Load request received for source=%s", request.source)

        # Step 1: Fetch raw stock data from Yahoo Finance
        raw_text = fetch_stock_data(request.source)

        if not raw_text:
            logger.warning("No data fetched for source=%s", request.source)

            raise HTTPException(
                status_code=404,
                detail="No data found for given source"
            )

        # Step 2: Convert raw text into document format
        documents = load_text_as_document(
            text=raw_text,
            source=request.source
        )

        # Step 3: Split documents into chunks
        chunks = split_documents(documents)

        if not chunks:
            logger.warning("No chunks generated for source=%s", request.source)

            raise HTTPException(
                status_code=400,
                detail="No chunks generated from document"
            )

        # Step 4: Store chunks in vector database
        store_documents(chunks, ticker=request.source)

        logger.info(
            "Documents stored successfully for source=%s, total_chunks=%d",
            request.source,
            len(chunks)
        )

        return {
            "status": "success",
            "message": "Documents stored successfully",
            "chunks": len(chunks)
        }

    except HTTPException:
        raise

    except Exception:
        logger.error(
            "Failed to load documents for source=%s",
            request.source,
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to load and store documents"
        )