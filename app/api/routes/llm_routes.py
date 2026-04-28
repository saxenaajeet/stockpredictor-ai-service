# app/api/routes/llm_routes.py

import logging

from fastapi import APIRouter, HTTPException

from app.core.llm import get_llm
from app.models.llm_models import AskRequest, AskResponse
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ask", response_model=AskResponse)
def ask_phi3(request: AskRequest):
    """
    Simple LLM query endpoint.

    Flow:
    1. Initialize LLM
    2. Invoke with user question
    3. Return response
    """

    try:
        logger.info("LLM request received")

        # Step 1: Initialize LLM
        logger.info("Initializing LLM with provider=%s", settings.provider)
        llm = get_llm(provider=settings.provider)

        # Step 2: Invoke LLM
        logger.info("Invoking LLM")
        result = llm.invoke(request.question)

        if not result or not getattr(result, "content", None):
            logger.warning("Empty response from LLM")

            raise HTTPException(
                status_code=502,
                detail="LLM returned empty response"
            )

        logger.info("LLM response generated successfully")

        # Step 3: Return response
        return AskResponse(answer=result.content)

    except HTTPException:
        raise

    except Exception:
        logger.error("LLM request failed", exc_info=True)

        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing LLM request"
        )