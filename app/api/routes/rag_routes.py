# app/api/routes/rag_routes.py

import logging

from fastapi import APIRouter, HTTPException

from app.models.rag_models import RagQueryRequest, RagQueryResponse
from app.core.chains import run_rag_pipeline

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/query", response_model=RagQueryResponse)
def query_rag(request: RagQueryRequest):
    """
    RAG query endpoint.

    Flow:
    1. Receive question + ticker
    2. Run RAG pipeline
    3. Return grounded answer
    """

    try:
        logger.info("RAG query received for ticker=%s", request.ticker)

        # Step 1: Execute RAG pipeline
        answer = run_rag_pipeline(
            question=request.question,
            ticker=request.ticker
        )

        if not answer:
            logger.warning("Empty RAG response for ticker=%s", request.ticker)

            raise HTTPException(
                status_code=502,
                detail="RAG pipeline returned empty response"
            )

        logger.info("RAG query completed successfully for ticker=%s", request.ticker)

        # Step 2: Return response
        return RagQueryResponse(
            question=request.question,
            answer=answer,
            status="success"
        )

    except HTTPException:
        raise

    except Exception:
        logger.error(
            "RAG query failed for ticker=%s",
            request.ticker,
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing RAG query"
        )