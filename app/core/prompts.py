from langchain_core.prompts import ChatPromptTemplate



stock_research_prompt = ChatPromptTemplate.from_template(
    """You are a professional stock research assistant.

Analyze the stock ticker: {ticker}

Provide your response strictly in this format:

Company: <what the company does in 1-2 lines>
Answer in a tabular format with the following sections:
Summary: <a concise summary of the stock's current situation>
Outlook: <bullish / bearish / neutral with reason>
Key Risks:
- <risk 1>
- <risk 2>
- <risk 3>
Simple View: <final recommendation in 1 line>

Keep the response concise and beginner-friendly.
"""
)

rag_query_prompt = ChatPromptTemplate.from_template(
    """
You are a helpful research assistant.

Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""
)

agent_prompt = ChatPromptTemplate.from_template(
"""
You are a stock analyst.

Use the following data:

RAG Knowledge:
{rag_data}

Latest Market Data:
{yahoo_data}

Question:
{question}

Answer clearly with risks and insights.
"""
)