from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from src.domain.document.models.document import Document


class TestDocument:
    def test_create_document_with_required_fields(self):
        document = Document(
            title="Test Document",
            content="This is test content",
        )

        assert document.title == "Test Document"
        assert document.content == "This is test content"
        assert document.source == ""
        assert isinstance(document.id, UUID)
        assert isinstance(document.created_at, datetime)
        assert isinstance(document.updated_at, datetime)

    def test_create_document_with_all_fields(self):
        test_id = UUID("123e4567-e89b-12d3-a456-426614174000")
        test_time = datetime(2024, 1, 1, 12, 0, 0)

        document = Document(
            id=test_id,
            title="Test Document",
            content="This is test content",
            source="test_source.pdf",
            created_at=test_time,
            updated_at=test_time,
        )

        assert document.id == test_id
        assert document.source == "test_source.pdf"
        assert document.created_at == test_time
        assert document.updated_at == test_time

    def test_empty_title_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            Document(title="", content="Test content")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("title",)
        assert "Document title cannot be empty" in errors[0]["msg"]

    def test_empty_content_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            Document(title="Test Title", content="")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("content",)
        assert "Document content cannot be empty" in errors[0]["msg"]

    def test_whitespace_only_title_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            Document(title="   ", content="Test content")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("title",)

    def test_update_content(self):
        document = Document(
            title="Test Document",
            content="Original content",
        )
        original_updated_at = document.updated_at

        document.update_content("New content")

        assert document.content == "New content"
        assert document.updated_at > original_updated_at
