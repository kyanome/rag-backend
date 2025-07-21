"""Document API routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.domain.document.models.document import Document
from src.presentation.api.dependencies import get_document_usecase
from src.usecase.document.document_usecase import DocumentUseCase

router = APIRouter()


class DocumentCreateRequest(BaseModel):
    """Request schema for creating a document."""

    title: str
    content: str
    source: str = ""


class DocumentUpdateRequest(BaseModel):
    """Request schema for updating a document."""

    content: str


class DocumentListResponse(BaseModel):
    """Response schema for document list."""

    documents: list[Document]
    total: int


class DeleteAllResponse(BaseModel):
    """Response schema for delete all operation."""

    deleted_count: int


@router.post("", response_model=Document)
async def create_document(
    request: DocumentCreateRequest,
    usecase: Annotated[DocumentUseCase, Depends(get_document_usecase)],
) -> Document:
    """Create a new document."""
    return await usecase.create(
        title=request.title,
        content=request.content,
        source=request.source,
    )


@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: UUID,
    usecase: Annotated[DocumentUseCase, Depends(get_document_usecase)],
) -> Document:
    """Get a document by ID."""
    document = await usecase.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    usecase: Annotated[DocumentUseCase, Depends(get_document_usecase)],
    limit: int = 100,
    offset: int = 0,
) -> DocumentListResponse:
    """List documents with pagination."""
    documents = await usecase.list(limit=limit, offset=offset)
    # For simplicity, return the count of fetched documents as total
    # In production, you'd want a separate count query
    return DocumentListResponse(documents=documents, total=len(documents))


@router.put("/{document_id}", response_model=Document)
async def update_document(
    document_id: UUID,
    request: DocumentUpdateRequest,
    usecase: Annotated[DocumentUseCase, Depends(get_document_usecase)],
) -> Document:
    """Update a document's content."""
    document = await usecase.update(document_id, request.content)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    usecase: Annotated[DocumentUseCase, Depends(get_document_usecase)],
) -> dict[str, bool]:
    """Delete a document by ID."""
    deleted = await usecase.delete(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"deleted": True}


@router.delete("", response_model=DeleteAllResponse)
async def delete_all_documents(
    usecase: Annotated[DocumentUseCase, Depends(get_document_usecase)],
) -> DeleteAllResponse:
    """Delete all documents."""
    count = await usecase.delete_all()
    return DeleteAllResponse(deleted_count=count)
