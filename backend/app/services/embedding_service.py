"""
Embedding Service
Generates embeddings for documents and queries
"""
import logging
from typing import List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Embedding service using OpenAI or other providers
    """
    
    def __init__(self):
        """Initialize embedding service"""
        self.model = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY.get_secret_value())
            logger.info(f"✅ Embedding service initialized with {self.model}")
        except Exception as e:
            logger.warning(f"Could not initialize OpenAI embedding: {e}")
            self.client = None
    
    def embed_text(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for a single text
        """
        if not self.client:
            logger.warning("Embedding service not available")
            return None
        
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            embedding = response.data[0].embedding
            
            logger.info(f"Generated embedding for text (length: {len(embedding)})")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def embed_texts(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Generate embeddings for multiple texts
        """
        if not self.client:
            logger.warning("Embedding service not available")
            return None
        
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            
            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.dimension


_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service(force_init: bool = False) -> Optional[EmbeddingService]:
    """Return a cached EmbeddingService instance, initializing on first call."""
    global _embedding_service
    if _embedding_service is None or force_init:
        try:
            _embedding_service = EmbeddingService()
        except Exception as e:
            logger.warning(f"Could not initialize embedding service: {e}")
            _embedding_service = None
    return _embedding_service
