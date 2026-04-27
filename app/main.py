from fastapi import FastAPI
from app.config import settings
from app.api.routes.stock_routes import router as stock_routes
from app.api.routes.rag_routes import router as rag_routes
from app.api.routes.llm_routes import router as llm_router
from app.api.routes.document_routes import router as document_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }

app.include_router(stock_routes, prefix="/stock", tags=["Stock"])
app.include_router(rag_routes, prefix="/rag", tags=["RAG"])
app.include_router(llm_router, prefix="/llm", tags=["LLM"])
app.include_router(document_router, prefix="/documents", tags=["Documents"])
