"""Dependency injection for FastAPI."""

import os
from typing import Annotated

from fastapi import Depends

from src.domain.document.repositories.document_repository import DocumentRepository
from src.domain.rag.services.rag_strategy import RAGStrategy
from src.infrastructure.algorithms.mock_rag_strategy import MockRAGStrategy
from src.infrastructure.algorithms.simple_rag_strategy import SimpleRAGStrategy
from src.infrastructure.config.settings import Settings, get_settings
from src.infrastructure.external.azure_openai_client import AzureOpenAIClient
from src.infrastructure.repositories.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
from src.usecase.document.document_usecase import DocumentUseCase
from src.usecase.rag.rag_query_usecase import RAGQueryUseCase

# Repository instances (singleton pattern for in-memory storage)
_document_repository: DocumentRepository | None = None
_azure_openai_client: AzureOpenAIClient | None = None


def get_document_repository() -> DocumentRepository:
    """Get document repository instance."""
    global _document_repository
    if _document_repository is None:
        _document_repository = InMemoryDocumentRepository()
    return _document_repository


def get_azure_openai_client(
    settings: Annotated[Settings, Depends(get_settings)],
) -> AzureOpenAIClient:
    """Get Azure OpenAI client instance."""
    global _azure_openai_client
    if _azure_openai_client is None:
        _azure_openai_client = AzureOpenAIClient(settings)
    return _azure_openai_client


def get_rag_strategy(
    document_repository: Annotated[
        DocumentRepository, Depends(get_document_repository)
    ],
    _settings: Annotated[Settings, Depends(get_settings)],
) -> RAGStrategy:
    """Get RAG strategy instance based on configuration."""
    # Use environment variable to switch between strategies
    strategy_type = os.getenv("RAG_STRATEGY", "simple")

    if strategy_type == "mock":
        return MockRAGStrategy(document_repository)
    else:
        # Default to SimpleRAGStrategy
        return SimpleRAGStrategy(document_repository)


def get_document_usecase(
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
) -> DocumentUseCase:
    """Get document use case instance."""
    return DocumentUseCase(repository)


def get_rag_query_usecase(
    rag_strategy: Annotated[RAGStrategy, Depends(get_rag_strategy)],
    openai_client: Annotated[AzureOpenAIClient, Depends(get_azure_openai_client)],
) -> RAGQueryUseCase:
    """Get RAG query use case instance."""
    return RAGQueryUseCase(rag_strategy, openai_client)
