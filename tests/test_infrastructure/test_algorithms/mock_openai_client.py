"""Mock OpenAI client for testing."""

from typing import Any

from src.infrastructure.config.settings import Settings
from src.infrastructure.external.azure_openai_client import AzureOpenAIClient


class MockOpenAIClient(AzureOpenAIClient):
    """Mock implementation of Azure OpenAI client for testing."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize mock client without requiring real Azure credentials."""
        # Don't call super().__init__ to avoid Azure authentication
        self.settings = settings or Settings(
            azure_openai_endpoint="https://mock.openai.azure.com/",
            azure_search_endpoint="https://mock.search.windows.net",
        )

    async def get_chat_completion(
        self,
        messages: list[Any],
        _model: str | None = None,
        _temperature: float = 0.7,
        _max_tokens: int = 1000,
    ) -> str:
        """Return mock chat completion."""
        # Extract the user's question from messages
        user_message = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        # Simple mock response based on the query
        if "no relevant documents" in user_message.lower():
            return "I couldn't find any relevant information to answer your question."

        return (
            f"This is a mock answer based on the provided context for: "
            f"{user_message[:50]}..."
        )

    async def get_embeddings(
        self,
        _text: str,
        _model: str | None = None,
    ) -> list[float]:
        """Return mock embeddings."""
        # Return a simple mock embedding vector
        return [0.1, 0.2, 0.3, 0.4, 0.5]
