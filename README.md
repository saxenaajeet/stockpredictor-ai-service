# StockPredictor AI Service

Python AI microservice for stock research, RAG, LangChain workflows, and MCP-based market data tools.

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check:

```bash
http://localhost:8000/health
```


API Endpoint	    Purpose	                            Input	                    Output
/llm/ask	        Basic LLM query	                    question	                Generic answer
/documents/load	    Load data into DB	                ticker/source	            Data stored
/documents/search	Retrieve chunks	                    ticker + question	        Matched chunks
/rag/query	        Answer using RAG	                ticker + question	        Grounded answer
/stock/research	    Structured stock report	            ticker	                    Formatted analysis
/agent/query	    Intelligent multi-source answer	    ticker + question	        Final reasoning answer

