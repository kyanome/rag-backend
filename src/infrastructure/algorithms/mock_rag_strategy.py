from src.domain.document.repositories.document_repository import DocumentRepository
from src.domain.rag.models.query import Query, QueryResult
from src.domain.rag.services.rag_strategy import RAGStrategy


class MockRAGStrategy(RAGStrategy):
    """Mock implementation of RAG strategy for testing and development."""

    def __init__(self, document_repository: DocumentRepository):
        super().__init__(document_repository)

    async def execute(self, query: Query) -> QueryResult:
        """
        Execute mock RAG query.

        This implementation:
        1. Gets a few documents from the repository
        2. Generates a mock answer based on the query
        3. Returns the result
        """
        # Get some documents (simulating search)
        documents = await self.document_repository.find_all(limit=query.top_k)

        # Generate mock answer
        if documents:
            doc_count = len(documents)
            answer = (
                f"Based on {doc_count} documents, "
                f"here's a mock answer for: '{query.text}'"
            )
            sources = [doc.source for doc in documents if doc.source]
        else:
            answer = f"No documents found to answer: '{query.text}'"
            sources = []

        return QueryResult(
            query=query,
            answer=answer,
            sources=sources[: query.top_k],  # Limit sources to top_k
        )
