import pytest

from src.domain.document.models.document import Document
from src.domain.rag.models.query import Query
from src.infrastructure.algorithms.mock_rag_strategy import MockRAGStrategy
from src.infrastructure.repositories.in_memory_document_repository import (
    InMemoryDocumentRepository,
)


class TestMockRAGStrategy:
    @pytest.fixture
    async def repository_with_documents(self):
        repository = InMemoryDocumentRepository()

        # Add some test documents
        docs = [
            Document(
                title="Python Programming",
                content="Python is a high-level programming language.",
                source="python_guide.pdf",
            ),
            Document(
                title="Machine Learning Basics",
                content="Machine learning is a subset of artificial intelligence.",
                source="ml_basics.pdf",
            ),
            Document(
                title="Data Science Introduction",
                content="Data science combines statistics and programming.",
                source="data_science_intro.pdf",
            ),
        ]

        for doc in docs:
            await repository.save(doc)

        return repository

    @pytest.fixture
    def empty_repository(self):
        return InMemoryDocumentRepository()

    async def test_execute_with_documents(self, repository_with_documents):
        strategy = MockRAGStrategy(repository_with_documents)
        query = Query(text="What is Python?")

        result = await strategy.execute(query)

        assert result.query == query
        assert "Based on 3 documents" in result.answer
        assert "What is Python?" in result.answer
        assert len(result.sources) == 3
        assert all(source.endswith(".pdf") for source in result.sources)

    async def test_execute_with_empty_repository(self, empty_repository):
        strategy = MockRAGStrategy(empty_repository)
        query = Query(text="What is Python?")

        result = await strategy.execute(query)

        assert result.query == query
        assert "No documents found" in result.answer
        assert "What is Python?" in result.answer
        assert result.sources == []

    async def test_execute_respects_top_k(self, repository_with_documents):
        strategy = MockRAGStrategy(repository_with_documents)
        query = Query(text="Tell me about AI", top_k=2)

        result = await strategy.execute(query)

        assert result.query == query
        assert "Based on 2 documents" in result.answer
        assert len(result.sources) == 2

    async def test_execute_with_documents_without_sources(self, empty_repository):
        # Add documents without sources
        docs = [
            Document(title="Doc 1", content="Content 1"),
            Document(title="Doc 2", content="Content 2"),
        ]
        for doc in docs:
            await empty_repository.save(doc)

        strategy = MockRAGStrategy(empty_repository)
        query = Query(text="Test query")

        result = await strategy.execute(query)

        assert "Based on 2 documents" in result.answer
        assert result.sources == []  # No sources since documents have empty sources
