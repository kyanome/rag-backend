"""Azure OpenAI client implementation using DefaultAzureCredential."""

from typing import Any

from azure.identity import DefaultAzureCredential
from openai import AsyncAzureOpenAI
from openai.types.chat import ChatCompletionMessageParam

from src.infrastructure.config.settings import Settings, get_settings


class AzureOpenAIClient:
    """Azure OpenAI client wrapper using DefaultAzureCredential."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize Azure OpenAI client.

        Args:
            settings: Optional settings instance. If not provided, will use
                get_settings().
        """
        self.settings = settings or get_settings()
        self.credential = DefaultAzureCredential()

        # Initialize the async client
        self.client = AsyncAzureOpenAI(
            azure_endpoint=self.settings.azure_openai_endpoint,
            api_version=self.settings.azure_openai_api_version,
            azure_ad_token_provider=self._get_token_provider(),
        )

    def _get_token_provider(self) -> Any:
        """Get token provider for Azure AD authentication."""
        from azure.identity.aio import (
            DefaultAzureCredential as AsyncDefaultAzureCredential,
        )

        async def token_provider() -> str:
            credential = AsyncDefaultAzureCredential()
            token = await credential.get_token(
                "https://cognitiveservices.azure.com/.default"
            )
            return token.token

        return token_provider

    async def get_chat_completion(
        self,
        messages: list[ChatCompletionMessageParam],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """Get chat completion from Azure OpenAI.

        Args:
            messages: List of chat messages
            model: Optional model deployment name. If not provided, uses default
                chat deployment.
            temperature: Temperature for response generation
            max_tokens: Maximum tokens in response

        Returns:
            The generated response text
        """
        deployment_name = model or self.settings.azure_openai_chat_deployment

        response = await self.client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content or ""

    async def get_embeddings(
        self,
        text: str,
        model: str | None = None,
    ) -> list[float]:
        """Get embeddings for text using Azure OpenAI.

        Args:
            text: Text to embed
            model: Optional model deployment name. If not provided, uses default
                embedding deployment.

        Returns:
            List of embedding values
        """
        deployment_name = model or self.settings.azure_openai_embedding_deployment

        response = await self.client.embeddings.create(
            model=deployment_name,
            input=text,
        )

        return response.data[0].embedding
