from abc import ABC, abstractmethod

from src.domain.document.models.document import Document


class RAGStrategy(ABC):
    """Abstract base class for RAG retrieval strategies."""

    @abstractmethod
    async def retrieve_documents(
        self, query_text: str, top_k: int = 5
    ) -> list[Document]:
        """
        Retrieve relevant documents for the given query.

        This method defines HOW to search for documents (e.g., keyword search,
        semantic search, hybrid search, etc.)

        Args:
            query_text: The query text
            top_k: Number of documents to retrieve

        Returns:
            List of relevant documents
        """
        pass
