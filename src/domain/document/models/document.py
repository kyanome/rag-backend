from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class Document(BaseModel):
    """Document entity for RAG system."""

    id: UUID = Field(default_factory=uuid4)
    title: str
    content: str
    source: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Document title cannot be empty")
        return v

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Document content cannot be empty")
        return v

    def update_content(self, content: str) -> None:
        """Update document content and timestamp."""
        self.content = content
        self.updated_at = datetime.now(UTC)
