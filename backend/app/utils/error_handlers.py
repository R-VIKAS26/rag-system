"""
Error handlers and exception utilities
"""
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc}")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__
        },
    )


class RAGException(Exception):
    """Base RAG exception"""
    pass


class DocumentProcessingError(RAGException):
    """Document processing error"""
    pass


class EmbeddingError(RAGException):
    """Embedding generation error"""
    pass


class VectorStoreError(RAGException):
    """Vector store operation error"""
    pass


class LLMError(RAGException):
    """LLM operation error"""
    pass


class AgentError(RAGException):
    """Agent operation error"""
    pass
