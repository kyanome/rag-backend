"""Document management use cases."""

from uuid import UUID

from src.domain.document.models.document import Document
from src.domain.document.repositories.document_repository import DocumentRepository


class DocumentUseCase:
    """Use case for document CRUD operations."""

    def __init__(self, document_repository: DocumentRepository) -> None:
        self._document_repository = document_repository

    async def create(self, title: str, content: str, source: str = "") -> Document:
        """Create and save a new document.

        Args:
            title: Document title
            content: Document content
            source: Document source (optional)

        Returns:
            The created document
        """
        document = Document(
            title=title,
            content=content,
            source=source,
        )
        return await self._document_repository.save(document)

    async def get(self, document_id: UUID) -> Document | None:
        """Get a document by ID.

        Args:
            document_id: The document ID

        Returns:
            The document if found, None otherwise
        """
        return await self._document_repository.find_by_id(document_id)

    async def list(self, limit: int = 100, offset: int = 0) -> list[Document]:
        """List documents with pagination.

        Args:
            limit: Maximum number of documents to return
            offset: Number of documents to skip

        Returns:
            List of documents
        """
        return await self._document_repository.find_all(limit=limit, offset=offset)

    async def update(self, document_id: UUID, content: str) -> Document | None:
        """Update a document's content.

        Args:
            document_id: The document ID
            content: New content

        Returns:
            The updated document if found, None otherwise
        """
        document = await self._document_repository.find_by_id(document_id)
        if not document:
            return None

        document.update_content(content)
        return await self._document_repository.update(document)

    async def delete(self, document_id: UUID) -> bool:
        """Delete a document.

        Args:
            document_id: The document ID

        Returns:
            True if deleted, False if not found
        """
        return await self._document_repository.delete(document_id)

    async def delete_all(self) -> int:
        """Delete all documents.

        Returns:
            Number of documents deleted
        """
        return await self._document_repository.delete_all()
