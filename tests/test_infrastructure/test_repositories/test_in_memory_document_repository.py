from datetime import UTC, datetime
from uuid import UUID

import pytest

from src.domain.document.models.document import Document
from src.infrastructure.repositories.in_memory_document_repository import (
    InMemoryDocumentRepository,
)


class TestInMemoryDocumentRepository:
    @pytest.fixture
    def repository(self):
        return InMemoryDocumentRepository()

    @pytest.fixture
    def sample_document(self):
        return Document(
            title="Test Document",
            content="This is test content",
            source="test.pdf",
        )

    async def test_save_document(self, repository, sample_document):
        saved_doc = await repository.save(sample_document)

        assert saved_doc == sample_document
        assert saved_doc.id == sample_document.id

    async def test_find_by_id(self, repository, sample_document):
        await repository.save(sample_document)

        found_doc = await repository.find_by_id(sample_document.id)

        assert found_doc == sample_document

    async def test_find_by_id_not_found(self, repository):
        random_id = UUID("12345678-1234-5678-1234-567812345678")

        found_doc = await repository.find_by_id(random_id)

        assert found_doc is None

    async def test_find_all_empty(self, repository):
        docs = await repository.find_all()

        assert docs == []

    async def test_find_all_with_documents(self, repository):
        docs = []
        for i in range(5):
            doc = Document(
                title=f"Document {i}",
                content=f"Content {i}",
                created_at=datetime(2024, 1, i + 1, tzinfo=UTC),
            )
            docs.append(doc)
            await repository.save(doc)

        found_docs = await repository.find_all()

        assert len(found_docs) == 5
        # Check they are sorted by created_at
        for i in range(1, 5):
            assert found_docs[i].created_at > found_docs[i - 1].created_at

    async def test_find_all_with_pagination(self, repository):
        for i in range(10):
            doc = Document(
                title=f"Document {i}",
                content=f"Content {i}",
            )
            await repository.save(doc)

        # Test limit
        docs_limit = await repository.find_all(limit=3)
        assert len(docs_limit) == 3

        # Test offset
        docs_offset = await repository.find_all(limit=3, offset=3)
        assert len(docs_offset) == 3

        # Test limit + offset beyond available
        docs_beyond = await repository.find_all(limit=5, offset=8)
        assert len(docs_beyond) == 2

    async def test_update_document(self, repository, sample_document):
        await repository.save(sample_document)

        # Update the document
        sample_document.update_content("Updated content")
        updated_doc = await repository.update(sample_document)

        assert updated_doc.content == "Updated content"

        # Verify the update persisted
        found_doc = await repository.find_by_id(sample_document.id)
        assert found_doc.content == "Updated content"

    async def test_update_nonexistent_document(self, repository):
        doc = Document(title="New", content="Content")

        with pytest.raises(ValueError, match=f"Document with id {doc.id} not found"):
            await repository.update(doc)

    async def test_delete_document(self, repository, sample_document):
        await repository.save(sample_document)

        result = await repository.delete(sample_document.id)

        assert result is True

        # Verify deletion
        found_doc = await repository.find_by_id(sample_document.id)
        assert found_doc is None

    async def test_delete_nonexistent_document(self, repository):
        random_id = UUID("12345678-1234-5678-1234-567812345678")

        result = await repository.delete(random_id)

        assert result is False

    async def test_delete_all(self, repository):
        # Add multiple documents
        for i in range(5):
            doc = Document(
                title=f"Document {i}",
                content=f"Content {i}",
            )
            await repository.save(doc)

        # Delete all
        count = await repository.delete_all()

        assert count == 5

        # Verify all deleted
        docs = await repository.find_all()
        assert len(docs) == 0
