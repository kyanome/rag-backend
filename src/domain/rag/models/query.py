from pydantic import BaseModel, Field, field_validator


class Query(BaseModel):
    """User query for RAG system."""

    text: str
    top_k: int = Field(default=5, ge=1, le=100)

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query text cannot be empty")
        return v.strip()


class QueryResult(BaseModel):
    """Result of RAG query execution."""

    query: Query
    answer: str
    sources: list[str] = Field(default_factory=list)
