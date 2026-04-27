from app.core.llm import get_llm
from app.core.prompts import stock_research_prompt
from app.core.prompts import rag_query_prompt


def get_stock_research_chain():
    llm = get_llm(provider="ollama")
    return stock_research_prompt | llm

def get_rag_query_chain():
    llm = get_llm(provider="ollama")
    return rag_query_prompt | llm