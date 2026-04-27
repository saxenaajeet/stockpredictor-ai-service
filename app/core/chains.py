from torchgen import context

from app.core.llm import get_llm
from app.core.prompts import stock_research_prompt
from app.core.prompts import rag_query_prompt
from app.config import settings
from app.ingestion.vector_search import search_similar_documents


def get_stock_research_chain():
    llm = get_llm(provider=settings.provider)
    return stock_research_prompt | llm

def get_rag_query_chain():
    llm = get_llm(provider=settings.provider)
    return rag_query_prompt | llm

def run_rag_pipeline(question: str, documents):
    # Step 1: retrieve relevant chunks
    matched_docs = search_similar_documents(
        documents=documents,
        query=question,
        k=3
    )

    # Step 2: build context
    context = "\n\n".join([doc.page_content for doc in matched_docs])

    print("=== CONTEXT ===")
    print(context)

    print("=== QUESTION ===")
    print(question)

    # Step 3: get chain
    chain = get_rag_query_chain()

    # Step 4: invoke
    result = chain.invoke({
        "question": question,
        "context": context
    })

    return result.content

