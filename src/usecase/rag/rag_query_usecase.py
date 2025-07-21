"""RAG query execution use case."""

from src.domain.rag.models.query import Query, QueryResult
from src.domain.rag.services.rag_strategy import RAGStrategy


class RAGQueryUseCase:
    """Use case for executing RAG queries."""

    def __init__(self, rag_strategy: RAGStrategy) -> None:
        self._rag_strategy = rag_strategy

    async def execute(self, query_text: str, top_k: int = 5) -> QueryResult:
        """Execute a RAG query.

        Args:
            query_text: The query text
            top_k: Number of relevant documents to retrieve (1-100)

        Returns:
            The query result with answer and sources
        """
        # Create query object with validation
        query = Query(text=query_text, top_k=top_k)

        # Execute RAG strategy
        result = await self._rag_strategy.execute(query)

        return result
