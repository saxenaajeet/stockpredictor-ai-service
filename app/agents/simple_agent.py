from app.core.llm import get_llm
from app.config import settings
from app.agents.tools import rag_tool, yahoo_tool
from app.core.prompts import agent_prompt


def run_agent(question: str, ticker: str):

    # Step 1: get LLM
    llm = get_llm(settings.embedding_provider)

    # Step 2: call tools
    rag_data = rag_tool(ticker, question)
    yahoo_data = yahoo_tool(ticker)

    # Step 3: create chain (prompt + llm)
    chain = agent_prompt | llm

    # Step 4: invoke with variables
    response = chain.invoke({
        "rag_data": rag_data,
        "yahoo_data": yahoo_data,
        "question": question
    })

    return response.content