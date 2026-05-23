"""
Main FastAPI application entry point
Implements enterprise-grade RAG system with agentic capabilities
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.security import setup_security
import app.api as routes
from app.utils.logging import setup_logging
from app.utils.monitoring import setup_monitoring
from app.utils.error_handlers import validation_exception_handler, general_exception_handler

# Setup logging
logger = setup_logging(__name__, settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting Enterprise RAG System")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    
    # Setup monitoring
    if settings.PROMETHEUS_ENABLED:
        setup_monitoring()
        logger.info("📊 Prometheus monitoring enabled")
    # Lazy-initialize external services to fail fast during startup
    try:
        from app.services.vector_store import get_chroma_store
        from app.services.embedding_service import get_embedding_service
        from app.services.llm_service import get_llm_service
        from app.services.rag_service import get_rag_service

        chroma = get_chroma_store()
        embedding = get_embedding_service()
        llm = get_llm_service()
        rag = get_rag_service()

        logger.info(f"Startup services: chroma={'ok' if chroma else 'missing'}, embedding={'ok' if embedding else 'missing'}, llm={'ok' if llm else 'missing'}, rag={'ok' if rag else 'missing'}")
    except Exception as e:
        logger.warning(f"One or more services failed to initialize during startup: {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Enterprise RAG System")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        docs_url="/api/docs" if not settings.ENVIRONMENT == "production" else None,
        redoc_url="/api/redoc" if not settings.ENVIRONMENT == "production" else None,
        openapi_url="/api/openapi.json" if not settings.ENVIRONMENT == "production" else None,
        lifespan=lifespan,
    )
    
    # Setup security
    setup_security(app)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    # Add trusted hosts middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "localhost:4200"]
    )
    
    # Exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Include routers
    app.include_router(routes.health_router, prefix="/api/health", tags=["Health"])
    app.include_router(routes.auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(routes.document_router, prefix="/api/documents", tags=["Documents"])
    app.include_router(routes.rag_router, prefix="/api/rag", tags=["RAG"])
    app.include_router(routes.agent_router, prefix="/api/agents", tags=["Agents"])
    app.include_router(routes.analytics_router, prefix="/api/analytics", tags=["Analytics"])
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": "Enterprise RAG System API",
            "version": settings.API_VERSION,
            "docs_url": "/api/docs",
        }
    
    logger.info("✅ FastAPI application configured successfully")
    return app


# Create application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS if settings.ENVIRONMENT == "production" else 1,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
