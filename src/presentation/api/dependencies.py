"""Dependency injection for FastAPI."""

from typing import Annotated

from fastapi import Depends

from src.domain.document.repositories.document_repository import DocumentRepository
from src.domain.rag.services.rag_strategy import RAGStrategy
from src.infrastructure.algorithms.mock_rag_strategy import MockRAGStrategy
from src.infrastructure.repositories.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
from src.usecase.document.document_usecase import DocumentUseCase
from src.usecase.rag.rag_query_usecase import RAGQueryUseCase

# Repository instances (singleton pattern for in-memory storage)
_document_repository: DocumentRepository | None = None


def get_document_repository() -> DocumentRepository:
    """Get document repository instance."""
    global _document_repository
    if _document_repository is None:
        _document_repository = InMemoryDocumentRepository()
    return _document_repository


def get_rag_strategy(
    document_repository: Annotated[
        DocumentRepository, Depends(get_document_repository)
    ],
) -> RAGStrategy:
    """Get RAG strategy instance."""
    return MockRAGStrategy(document_repository)


def get_document_usecase(
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
) -> DocumentUseCase:
    """Get document use case instance."""
    return DocumentUseCase(repository)


def get_rag_query_usecase(
    rag_strategy: Annotated[RAGStrategy, Depends(get_rag_strategy)],
) -> RAGQueryUseCase:
    """Get RAG query use case instance."""
    return RAGQueryUseCase(rag_strategy)
