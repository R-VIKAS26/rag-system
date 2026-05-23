"""API route modules"""
from .health import router as health_router
from .auth import router as auth_router
from .documents import router as document_router
from .rag import router as rag_router
from .agents import router as agent_router
from .analytics import router as analytics_router

__all__ = [
    "health_router",
    "auth_router",
    "document_router",
    "rag_router",
    "agent_router",
    "analytics_router",
]
