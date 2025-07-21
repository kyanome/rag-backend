from uuid import UUID

from src.domain.document.models.document import Document
from src.domain.document.repositories.document_repository import DocumentRepository


class InMemoryDocumentRepository(DocumentRepository):
    """In-memory implementation of DocumentRepository for testing and development."""

    def __init__(self) -> None:
        self._documents: dict[UUID, Document] = {}

    async def save(self, document: Document) -> Document:
        """Save a document to the repository."""
        self._documents[document.id] = document
        return document

    async def find_by_id(self, document_id: UUID) -> Document | None:
        """Find a document by its ID."""
        return self._documents.get(document_id)

    async def find_all(self, limit: int = 100, offset: int = 0) -> list[Document]:
        """Find all documents with pagination."""
        all_docs = list(self._documents.values())
        # Sort by created_at for consistent ordering
        all_docs.sort(key=lambda d: d.created_at)
        return all_docs[offset : offset + limit]

    async def update(self, document: Document) -> Document:
        """Update an existing document."""
        if document.id not in self._documents:
            raise ValueError(f"Document with id {document.id} not found")
        self._documents[document.id] = document
        return document

    async def delete(self, document_id: UUID) -> bool:
        """Delete a document by its ID."""
        if document_id in self._documents:
            del self._documents[document_id]
            return True
        return False

    async def delete_all(self) -> int:
        """Delete all documents and return the count of deleted documents."""
        count = len(self._documents)
        self._documents.clear()
        return count
