"""
RAG Service
Core RAG functionality combining documents, embeddings, and LLM
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.services.vector_store import get_chroma_store
from app.services.embedding_service import get_embedding_service
from app.services.llm_service import get_llm_service
from app.core.config import settings

logger = logging.getLogger(__name__)


class RAGService:
    """
    Retrieval-Augmented Generation service
    Combines document retrieval with LLM generation
    """
    
    def __init__(self):
        """Initialize RAG service (lazy bindings to dependencies)."""
        self.chroma_store = get_chroma_store()
        self.embedding_service = get_embedding_service()
        self.llm_service = get_llm_service()
        logger.info("✅ RAG service initialized (dependencies bound lazily)")
    
    def add_documents(
        self,
        document_id: str,
        documents: List[str],
        metadatas: List[Dict],
        user_id: str
    ) -> None:
        """
        Add documents to RAG system
        """
        if not self.chroma_store:
            raise ValueError("Vector store not initialized")
        
        try:
            # Create collection for user
            collection_name = f"user_{user_id}"
            
            # Generate IDs
            ids = [f"{document_id}_chunk_{i}" for i in range(len(documents))]
            
            # Add metadata
            enriched_metadatas = [
                {
                    **meta,
                    "document_id": document_id,
                    "user_id": user_id,
                    "added_at": datetime.utcnow().isoformat()
                }
                for meta in metadatas
            ]
            
            # Add to vector store
            self.chroma_store.add_documents(
                collection_name=collection_name,
                documents=documents,
                metadatas=enriched_metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} chunks for document {document_id}")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def query_documents(
        self,
        query: str,
        user_id: str,
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Query documents using similarity search
        """
        if not self.chroma_store:
            raise ValueError("Vector store not initialized")
        
        try:
            collection_name = f"user_{user_id}"
            top_k = top_k or settings.RAG_TOP_K
            
            results = self.chroma_store.search(
                collection_name=collection_name,
                query_text=query,
                top_k=top_k
            )
            
            # Format results
            formatted_results = [
                {
                    "content": doc,
                    "score": score,
                    "metadata": meta
                }
                for doc, score, meta in results
            ]
            
            logger.info(f"Query returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying documents: {e}")
            raise
    
    def generate_answer(
        self,
        query: str,
        context: List[str],
        **kwargs
    ) -> str:
        """
        Generate answer using LLM with context
        """
        if not self.llm_service:
            raise ValueError("LLM service not initialized")
        
        try:
            # Build prompt with context
            prompt = self._build_prompt(query, context)
            
            # Generate answer
            answer = self.llm_service.generate(prompt, **kwargs)
            
            return answer
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise
    
    def rag_query(
        self,
        query: str,
        user_id: str,
        top_k: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Full RAG query: retrieve documents and generate answer
        """
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Retrieve relevant documents
            retrieved_docs = self.query_documents(
                query=query,
                user_id=user_id,
                top_k=top_k
            )
            
            # Extract content
            context = [doc["content"] for doc in retrieved_docs]
            
            # Step 2: Generate answer
            answer = self.generate_answer(query, context, **kwargs)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return {
                "query": query,
                "answer": answer,
                "sources": retrieved_docs,
                "processing_time": processing_time,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            raise
    
    @staticmethod
    def _build_prompt(query: str, context: List[str]) -> str:
        """
        Build prompt with context and query
        """
        context_text = "\n\n".join(context)
        
        prompt = f"""You are a helpful AI assistant. Answer the following question based on the provided context.

Context:
{context_text}

Question: {query}

Answer:"""
        
        return prompt


_rag_service: Optional[RAGService] = None


def get_rag_service(force_init: bool = False) -> Optional[RAGService]:
    global _rag_service
    if _rag_service is None or force_init:
        try:
            _rag_service = RAGService()
        except Exception as e:
            logger.warning(f"Could not initialize RAG service: {e}")
            _rag_service = None
    return _rag_service
