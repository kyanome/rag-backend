"""Tests for DocumentUseCase."""

from uuid import uuid4

import pytest

from src.infrastructure.repositories.in_memory_document_repository import (
    InMemoryDocumentRepository,
)
from src.usecase.document.document_usecase import DocumentUseCase


@pytest.fixture
async def document_usecase():
    """Create DocumentUseCase with in-memory repository."""
    repository = InMemoryDocumentRepository()
    return DocumentUseCase(repository)


@pytest.mark.asyncio
async def test_create_document(document_usecase):
    """Test creating a document."""
    # Create document
    document = await document_usecase.create(
        title="Test Document",
        content="Test content",
        source="test.txt",
    )

    # Verify document was created
    assert document.title == "Test Document"
    assert document.content == "Test content"
    assert document.source == "test.txt"
    assert document.id is not None


@pytest.mark.asyncio
async def test_get_document(document_usecase):
    """Test getting a document by ID."""
    # Create document
    created = await document_usecase.create(
        title="Test Document",
        content="Test content",
    )

    # Get document
    retrieved = await document_usecase.get(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.title == "Test Document"

    # Get non-existent document
    non_existent = await document_usecase.get(uuid4())
    assert non_existent is None


@pytest.mark.asyncio
async def test_list_documents(document_usecase):
    """Test listing documents with pagination."""
    # Create multiple documents
    for i in range(5):
        await document_usecase.create(
            title=f"Document {i}",
            content=f"Content {i}",
        )

    # List all documents
    documents = await document_usecase.list()
    assert len(documents) == 5

    # List with limit
    documents = await document_usecase.list(limit=3)
    assert len(documents) == 3

    # List with offset
    documents = await document_usecase.list(limit=2, offset=3)
    assert len(documents) == 2
    assert documents[0].title == "Document 3"


@pytest.mark.asyncio
async def test_update_document(document_usecase):
    """Test updating a document."""
    # Create document
    created = await document_usecase.create(
        title="Original Title",
        content="Original content",
    )
    original_updated_at = created.updated_at

    # Update document
    updated = await document_usecase.update(
        document_id=created.id,
        content="Updated content",
    )
    assert updated is not None
    assert updated.content == "Updated content"
    assert updated.title == "Original Title"  # Title unchanged
    assert updated.updated_at > original_updated_at

    # Update non-existent document
    non_existent = await document_usecase.update(
        document_id=uuid4(),
        content="New content",
    )
    assert non_existent is None


@pytest.mark.asyncio
async def test_delete_document(document_usecase):
    """Test deleting a document."""
    # Create document
    created = await document_usecase.create(
        title="To Delete",
        content="Will be deleted",
    )

    # Delete document
    deleted = await document_usecase.delete(created.id)
    assert deleted is True

    # Verify document is gone
    retrieved = await document_usecase.get(created.id)
    assert retrieved is None

    # Delete non-existent document
    deleted = await document_usecase.delete(uuid4())
    assert deleted is False


@pytest.mark.asyncio
async def test_delete_all_documents(document_usecase):
    """Test deleting all documents."""
    # Create multiple documents
    for i in range(3):
        await document_usecase.create(
            title=f"Document {i}",
            content=f"Content {i}",
        )

    # Delete all
    count = await document_usecase.delete_all()
    assert count == 3

    # Verify all are gone
    documents = await document_usecase.list()
    assert len(documents) == 0
