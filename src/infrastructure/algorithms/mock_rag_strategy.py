from src.domain.document.models.document import Document
from src.domain.document.repositories.document_repository import DocumentRepository
from src.domain.rag.services.rag_strategy import RAGStrategy


class MockRAGStrategy(RAGStrategy):
    """Mock implementation of RAG strategy for testing and development."""

    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    async def retrieve_documents(
        self, _query_text: str, top_k: int = 5
    ) -> list[Document]:
        """
        Retrieve documents using mock logic.

        For testing purposes, this just returns the first top_k documents.

        Args:
            query_text: The query text (not used in mock)
            top_k: Number of documents to retrieve

        Returns:
            List of mock documents
        """
        # Mock implementation: just return first top_k documents
        documents = await self.document_repository.find_all(limit=top_k)
        return documents
