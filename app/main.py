import logging

from fastapi import FastAPI

from app.api.routes.agent_routes import router as agent_router
from app.api.routes.stock_routes import router as stock_routes
from app.api.routes.rag_routes import router as rag_routes
from app.api.routes.llm_routes import router as llm_router
from app.api.routes.document_routes import router as document_router

from app.config import settings
from app.core.logging_config import setup_logging

# Initialize logging once at startup
setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)


@app.on_event("startup")
def on_startup():
    logger.info(
        "Starting application: %s | env=%s | version=%s",
        settings.app_name,
        settings.environment,
        settings.app_version
    )


@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down application: %s", settings.app_name)


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Used for readiness/liveness probes.
    """
    try:
        return {
            "status": "ok",
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment
        }
    except Exception:
        logger.error("Health check failed", exc_info=True)
        return {
            "status": "error"
        }


# Register routers
app.include_router(stock_routes, prefix="/stock", tags=["Stock"])
app.include_router(rag_routes, prefix="/rag", tags=["RAG"])
app.include_router(llm_router, prefix="/llm", tags=["LLM"])
app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(agent_router, prefix="/agent", tags=["Agent"])