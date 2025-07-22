import pytest

from src.domain.document.models.document import Document
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

    async def test_retrieve_documents_with_documents(self, repository_with_documents):
        strategy = MockRAGStrategy(repository_with_documents)

        documents = await strategy.retrieve_documents("What is Python?", top_k=5)

        assert len(documents) == 3
        assert all(isinstance(doc, Document) for doc in documents)
        assert documents[0].title == "Python Programming"

    async def test_retrieve_documents_with_empty_repository(self, empty_repository):
        strategy = MockRAGStrategy(empty_repository)

        documents = await strategy.retrieve_documents("What is Python?", top_k=5)

        assert documents == []

    async def test_retrieve_documents_respects_top_k(self, repository_with_documents):
        strategy = MockRAGStrategy(repository_with_documents)

        documents = await strategy.retrieve_documents("Tell me about AI", top_k=2)

        assert len(documents) == 2

    async def test_retrieve_documents_query_text_ignored(
        self, repository_with_documents
    ):
        # Mock strategy doesn't use query_text, just returns documents
        strategy = MockRAGStrategy(repository_with_documents)

        documents1 = await strategy.retrieve_documents("Python", top_k=3)
        documents2 = await strategy.retrieve_documents("Java", top_k=3)

        # Should return same documents regardless of query
        assert len(documents1) == len(documents2) == 3
        assert [d.id for d in documents1] == [d.id for d in documents2]
