"""
Chroma DB Vector Store Service
Manages vector embeddings and similarity search
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    """
    Chroma DB vector store wrapper
    Handles embeddings and similarity search
    """
    
    def __init__(self):
        """Initialize Chroma DB client"""
        try:
            # Create persistent Chroma client
            self.settings = ChromaSettings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=settings.CHROMA_DB_PATH,
                anonymized_telemetry=False,
            )
            
            self.client = chromadb.Client(self.settings)
            logger.info("✅ Chroma DB initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Chroma DB: {e}")
            raise
    
    def create_collection(self, name: str, metadata: Optional[Dict] = None) -> Any:
        """
        Create a new collection
        """
        try:
            collection = self.client.create_collection(
                name=name,
                metadata=metadata or {"source": "rag_system"}
            )
            logger.info(f"Collection created: {name}")
            return collection
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise
    
    def get_or_create_collection(self, name: str) -> Any:
        """
        Get existing collection or create new one
        """
        try:
            collection = self.client.get_or_create_collection(
                name=name,
                metadata={"source": "rag_system"}
            )
            return collection
        except Exception as e:
            logger.error(f"Error getting collection: {e}")
            raise
    
    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str]
    ) -> None:
        """
        Add documents to collection
        """
        try:
            collection = self.get_or_create_collection(collection_name)
            
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(documents)} documents to {collection_name}")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def search(
        self,
        collection_name: str,
        query_text: str,
        top_k: int = 5
    ) -> List[Tuple[str, float, Dict]]:
        """
        Search for similar documents
        Returns list of (text, distance, metadata)
        """
        try:
            collection = self.get_or_create_collection(collection_name)
            
            results = collection.query(
                query_texts=[query_text],
                n_results=top_k
            )
            
            # Process results
            documents = results['documents'][0]
            distances = results['distances'][0]
            metadatas = results['metadatas'][0]
            
            # Convert distances to similarity scores (1 - distance)
            search_results = [
                (doc, 1 - dist, meta)
                for doc, dist, meta in zip(documents, distances, metadatas)
            ]
            
            logger.info(f"Search completed, found {len(search_results)} results")
            return search_results
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            raise
    
    def delete_collection(self, name: str) -> None:
        """
        Delete a collection
        """
        try:
            self.client.delete_collection(name=name)
            logger.info(f"Collection deleted: {name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise
    
    def list_collections(self) -> List[str]:
        """
        List all collections
        """
        try:
            collections = self.client.list_collections()
            names = [c.name for c in collections]
            return names
        except Exception as e:
            logger.error(f"Error listing collections: {e}")
            raise
    
    def persist(self) -> None:
        """
        Persist data to disk
        """
        try:
            self.client.persist()
            logger.info("Chroma DB persisted to disk")
        except Exception as e:
            logger.error(f"Error persisting data: {e}")
            raise


_chroma_store: Optional[ChromaVectorStore] = None


def get_chroma_store(force_init: bool = False) -> Optional[ChromaVectorStore]:
    """Return a cached ChromaVectorStore instance, initializing on first call.

    If initialization fails, None is returned and a warning is logged.
    """
    global _chroma_store
    if _chroma_store is None or force_init:
        try:
            _chroma_store = ChromaVectorStore()
        except Exception as e:
            logger.warning(f"Could not initialize Chroma DB: {e}")
            _chroma_store = None
    return _chroma_store
