from abc import ABC, abstractmethod

from src.domain.document.repositories.document_repository import DocumentRepository
from src.domain.rag.models.query import Query, QueryResult


class RAGStrategy(ABC):
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    @abstractmethod
    async def execute(self, query: Query) -> QueryResult:
        """
        Execute RAG query and return the result.

        This method should:
        1. Generate embedding for the query
        2. Search for relevant documents using document_repository
        3. Generate answer based on the documents
        4. Return the complete result
        """
        pass
