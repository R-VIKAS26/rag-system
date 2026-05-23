"""
Document management endpoints
Handles document upload, processing, and management
"""
import logging
import os
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path

from app.core.config import settings

from app.core.security import get_current_user, TokenData
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


class DocumentInfo(BaseModel):
    """Document information"""
    document_id: str
    filename: str
    file_type: str
    file_size: int
    upload_date: datetime
    status: str


class DocumentUploadResponse(BaseModel):
    """Document upload response"""
    document_id: str
    filename: str
    status: str
    message: str


class DocumentListResponse(BaseModel):
    """Document list response"""
    documents: List[DocumentInfo]
    total: int


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Document"
)
async def upload_document(
    file: UploadFile = File(...),
    current_user: TokenData = Depends(get_current_user)
) -> DocumentUploadResponse:
    """
    Upload a document (PDF, Excel, CSV, etc.)
    """
    logger.info(f"Document upload request from user: {current_user.user_id}")
    
    # Validate file extension
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type .{file_ext} not allowed"
        )
    
    # Validate file size
    file_size = len(await file.read())
    await file.seek(0)  # Reset file pointer
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds maximum allowed size"
        )
    
    # TODO: Save file and process with RAG
    document_id = f"doc_{int(datetime.utcnow().timestamp())}"

    # Save file to storage
    storage_dir = Path("./storage")
    storage_dir.mkdir(parents=True, exist_ok=True)
    saved_name = f"{document_id}_{file.filename}"
    saved_path = storage_dir / saved_name

    contents = await file.read()
    try:
        with open(saved_path, "wb") as f:
            f.write(contents)
    finally:
        await file.close()

    # Process document (sync for now)
    try:
        from app.utils.document_processor import DocumentProcessor
        from app.services.vector_store import get_chroma_store
        from app.services.embedding_service import get_embedding_service

        result = DocumentProcessor.process_document(str(saved_path))

        # If we have a vector store, chunk and add documents
        text_content = result.get("content") or str(result.get("data") or "")

        def chunk_text(text: str, size: int, overlap: int) -> List[str]:
            chunks: List[str] = []
            start = 0
            text_len = len(text)
            while start < text_len:
                end = min(start + size, text_len)
                chunks.append(text[start:end])
                start = end - overlap if end - overlap > start else end
            return chunks

        chunks = chunk_text(text_content, settings.RAG_CHUNK_SIZE, settings.RAG_CHUNK_OVERLAP)

        chroma = get_chroma_store()
        embedding = get_embedding_service()

        if chroma:
            collection_name = f"user_{current_user.user_id}"
            metadatas = [{"filename": file.filename, "document_id": document_id} for _ in chunks]
            ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
            try:
                chroma.add_documents(collection_name, chunks, metadatas, ids)
                chroma.persist()
            except Exception as e:
                logger.warning(f"Failed to add documents to Chroma: {e}")

    except Exception as e:
        logger.error(f"Error processing uploaded document: {e}")

    logger.info(f"Document uploaded and saved: {saved_path}")

    return DocumentUploadResponse(
        document_id=document_id,
        filename=file.filename,
        status="processing",
        message="Document received and processing started"
    )


@router.get(
    "/",
    response_model=DocumentListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Documents"
)
async def list_documents(
    skip: int = 0,
    limit: int = 10,
    current_user: TokenData = Depends(get_current_user)
) -> DocumentListResponse:
    """
    List all documents for the current user
    """
    logger.info(f"Document list request from user: {current_user.user_id}")
    
    # TODO: Fetch documents from database
    documents = []
    
    return DocumentListResponse(
        documents=documents,
        total=len(documents)
    )


@router.get(
    "/{document_id}",
    response_model=DocumentInfo,
    status_code=status.HTTP_200_OK,
    summary="Get Document Details"
)
async def get_document(
    document_id: str,
    current_user: TokenData = Depends(get_current_user)
) -> DocumentInfo:
    """
    Get details for a specific document
    """
    logger.info(f"Document details request: {document_id}")
    
    # TODO: Fetch document from database
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found"
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Document"
)
async def delete_document(
    document_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Delete a document
    """
    logger.info(f"Document deletion request: {document_id}")
    
    # TODO: Delete document from database and vector store
    logger.info(f"Document deleted: {document_id}")
    return None
