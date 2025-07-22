"""Simple RAG strategy implementation."""

from src.domain.document.models.document import Document
from src.domain.document.repositories.document_repository import DocumentRepository
from src.domain.rag.services.rag_strategy import RAGStrategy


class SimpleRAGStrategy(RAGStrategy):
    """Simple RAG strategy that retrieves all documents without sophisticated search."""

    def __init__(self, document_repository: DocumentRepository) -> None:
        """Initialize the simple RAG strategy.

        Args:
            document_repository: Repository for document operations
        """
        self.document_repository = document_repository

    async def retrieve_documents(
        self, _query_text: str, top_k: int = 5
    ) -> list[Document]:
        """
        Retrieve documents using a simple strategy.

        This simple implementation just returns the most recent documents.
        In a real implementation, you might add keyword matching or other
        simple filtering logic.

        Args:
            query_text: The query text (not used in this simple implementation)
            top_k: Number of documents to retrieve

        Returns:
            List of documents
        """
        # Simple implementation: just return the most recent documents
        documents = await self.document_repository.find_all(limit=top_k)
        return documents
