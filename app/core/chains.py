from torchgen import context

from app.core.llm import get_llm
from app.core.prompts import stock_research_prompt
from app.core.prompts import rag_query_prompt
from app.config import settings
from app.retrieval.search import search_similar_chunks


def get_stock_research_chain():
    llm = get_llm(provider=settings.embedding_provider)
    return stock_research_prompt | llm

def get_rag_query_chain():
    llm = get_llm(provider=settings.embedding_provider)
    return rag_query_prompt | llm

def run_rag_pipeline(question: str, ticker: str):

    matched_chunks = search_similar_chunks(
        query=question,
        ticker=ticker,
        k=5
    )

    context = "\n\n".join(matched_chunks)

    print("🔹 Retrieved Context:\n", context)

    chain = get_rag_query_chain()

    result = chain.invoke({
        "question": question,
        "context": context
    })

    return result.content

