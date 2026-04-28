import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.simple_agent import run_agent

router = APIRouter()
logger = logging.getLogger(__name__)


# Request schema (better than raw dict)
class AgentRequest(BaseModel):
    question: str
    ticker: str


@router.post("/query")
def agent_query(request: AgentRequest):
    """
    API endpoint to query the agent.

    Flow:
    1. Validate request
    2. Call agent
    3. Return response
    """

    try:
        logger.info("Received agent query for ticker=%s", request.ticker)

        # Step 1: Call agent
        answer = run_agent(
            question=request.question,
            ticker=request.ticker
        )

        logger.info("Agent query completed successfully for ticker=%s", request.ticker)

        # Step 2: Return response
        return {
            "status": "success",
            "answer": answer
        }

    except Exception:
        logger.error(
            "Agent query failed for ticker=%s",
            request.ticker,
            exc_info=True
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing request"
        )