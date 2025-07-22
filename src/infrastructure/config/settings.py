"""Application settings and configuration."""

from functools import lru_cache

from pydantic_settings import (  # type: ignore[import-untyped]
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra environment variables like RAG_STRATEGY
    )

    # Azure OpenAI Configuration (using DefaultAzureCredential)
    azure_openai_endpoint: str = "https://example.openai.azure.com/"
    azure_openai_api_version: str = "2024-02-01"

    # Model deployment names (can be customized per environment)
    azure_openai_chat_deployment: str = "gpt-35-turbo"  # For chat/completion
    azure_openai_embedding_deployment: str = "text-embedding-ada-002"  # For embeddings

    # Azure Cognitive Search Configuration (using DefaultAzureCredential)
    azure_search_endpoint: str = "https://example.search.windows.net"
    azure_search_index_name: str = "documents"

    # Application Configuration
    log_level: str = "INFO"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
