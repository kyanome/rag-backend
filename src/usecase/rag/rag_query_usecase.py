"""RAG query execution use case."""

from typing import Any

from src.domain.rag.models.query import Query, QueryResult
from src.domain.rag.services.rag_strategy import RAGStrategy
from src.infrastructure.external.azure_openai_client import AzureOpenAIClient


class RAGQueryUseCase:
    """Use case for executing RAG queries - orchestrates retrieval and generation."""

    def __init__(
        self,
        rag_strategy: RAGStrategy,
        openai_client: AzureOpenAIClient,
    ) -> None:
        """Initialize the RAG query use case.

        Args:
            rag_strategy: Strategy for retrieving documents
            openai_client: Azure OpenAI client for answer generation
        """
        self._rag_strategy = rag_strategy
        self._openai_client = openai_client

    async def execute(self, query_text: str, top_k: int = 5) -> QueryResult:
        """Execute a RAG query by orchestrating retrieval and generation.

        This method:
        1. Validates the query
        2. Retrieves relevant documents using the strategy
        3. Generates an answer using Azure OpenAI
        4. Returns the complete result

        Args:
            query_text: The query text
            top_k: Number of relevant documents to retrieve (1-100)

        Returns:
            The query result with answer and sources
        """
        # Create query object with validation
        query = Query(text=query_text, top_k=top_k)

        # Step 1: Retrieve documents using the strategy
        documents = await self._rag_strategy.retrieve_documents(
            query.text,
            query.top_k,
        )

        # Step 2: Generate answer using Azure OpenAI
        if not documents:
            answer = "No relevant documents found to answer your question."
        else:
            # Create context from documents
            context_parts = []
            for doc in documents:
                context_parts.append(f"Title: {doc.title}\nContent: {doc.content}")

            context = "\n\n---\n\n".join(context_parts)

            # Create prompt for Azure OpenAI
            system_prompt = (
                "You are a helpful assistant that answers questions based on the "
                "provided context. If the answer cannot be found in the context, "
                "say so clearly. Be concise and accurate in your responses."
            )

            user_prompt = f"""Context:
{context}

Question: {query_text}

Please provide a comprehensive answer based on the context above."""

            messages: list[Any] = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            # Generate answer
            answer = await self._openai_client.get_chat_completion(
                messages,
                None,  # model
                0.3,  # temperature - Lower for more factual responses
                500,  # max_tokens
            )

        # Step 3: Extract sources from documents
        sources = []
        for doc in documents:
            if doc.source:
                sources.append(doc.source)
            else:
                sources.append(f"{doc.title} (ID: {doc.id})")

        return QueryResult(
            query=query,
            answer=answer.strip(),
            sources=sources[: query.top_k],  # Limit sources to top_k
        )
