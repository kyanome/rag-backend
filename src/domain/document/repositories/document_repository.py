from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.document.models.document import Document


class DocumentRepository(ABC):
    @abstractmethod
    async def save(self, document: Document) -> Document:
        """Save a document to the repository."""
        pass

    @abstractmethod
    async def find_by_id(self, document_id: UUID) -> Document | None:
        """Find a document by its ID."""
        pass

    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> list[Document]:
        """Find all documents with pagination."""
        pass

    @abstractmethod
    async def search_by_embedding(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[Document]:
        """Search documents by embedding similarity."""
        pass

    @abstractmethod
    async def update(self, document: Document) -> Document:
        """Update an existing document."""
        pass

    @abstractmethod
    async def delete(self, document_id: UUID) -> bool:
        """Delete a document by its ID."""
        pass

    @abstractmethod
    async def delete_all(self) -> int:
        """Delete all documents and return the count of deleted documents."""
        pass
