from fastapi import APIRouter
from app.agents.simple_agent import run_agent

router = APIRouter()


@router.post("/query")
def agent_query(request: dict):

    answer = run_agent(
        question=request["question"],
        ticker=request["ticker"]
    )

    return {
        "answer": answer,
        "status": "success"
    }