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
