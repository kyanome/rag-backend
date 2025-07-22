"""Tests for RAGQueryUseCase."""

import pytest

from src.domain.document.models.document import Document
from src.domain.rag.models.query import QueryResult
from src.infrastructure.algorithms.mock_rag_strategy import MockRAGStrategy
from src.infrastructure.repositories.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
from src.usecase.rag.rag_query_usecase import RAGQueryUseCase
from tests.test_infrastructure.test_algorithms.mock_openai_client import (
    MockOpenAIClient,
)


@pytest.fixture
async def rag_query_usecase():
    """Create RAGQueryUseCase with mock strategy and mock OpenAI client."""
    repository = InMemoryDocumentRepository()
    # Add some test documents
    await repository.save(
        Document(
            title="Test Document",
            content="This is test content",
            source="test.pdf",
        )
    )
    strategy = MockRAGStrategy(repository)
    openai_client = MockOpenAIClient()
    return RAGQueryUseCase(strategy, openai_client)


@pytest.mark.asyncio
async def test_execute_rag_query(rag_query_usecase):
    """Test executing a RAG query."""
    # Execute query
    result = await rag_query_usecase.execute(
        query_text="What is machine learning?",
        top_k=3,
    )

    # Verify result
    assert isinstance(result, QueryResult)
    assert result.query.text == "What is machine learning?"
    assert result.query.top_k == 3
    assert isinstance(result.answer, str)
    assert len(result.answer) > 0
    assert isinstance(result.sources, list)


@pytest.mark.asyncio
async def test_execute_rag_query_with_default_top_k(rag_query_usecase):
    """Test executing a RAG query with default top_k."""
    # Execute query without specifying top_k
    result = await rag_query_usecase.execute(
        query_text="Explain neural networks",
    )

    # Verify result uses default top_k
    assert result.query.top_k == 5


@pytest.mark.asyncio
async def test_execute_rag_query_with_empty_text():
    """Test executing a RAG query with empty text."""
    repository = InMemoryDocumentRepository()
    strategy = MockRAGStrategy(repository)
    openai_client = MockOpenAIClient()
    usecase = RAGQueryUseCase(strategy, openai_client)

    # Should raise validation error
    with pytest.raises(ValueError, match="Query text cannot be empty"):
        await usecase.execute(query_text="")

    with pytest.raises(ValueError, match="Query text cannot be empty"):
        await usecase.execute(query_text="   ")


@pytest.mark.asyncio
async def test_execute_rag_query_with_invalid_top_k():
    """Test executing a RAG query with invalid top_k."""
    repository = InMemoryDocumentRepository()
    strategy = MockRAGStrategy(repository)
    openai_client = MockOpenAIClient()
    usecase = RAGQueryUseCase(strategy, openai_client)

    # Should raise validation error for top_k < 1
    with pytest.raises(ValueError):
        await usecase.execute(
            query_text="Test query",
            top_k=0,
        )

    # Should raise validation error for top_k > 100
    with pytest.raises(ValueError):
        await usecase.execute(
            query_text="Test query",
            top_k=101,
        )
