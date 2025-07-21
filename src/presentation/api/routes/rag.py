"""RAG API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from src.domain.rag.models.query import Query, QueryResult
from src.presentation.api.dependencies import get_rag_query_usecase
from src.usecase.rag.rag_query_usecase import RAGQueryUseCase

router = APIRouter()


@router.post("/query", response_model=QueryResult)
async def execute_rag_query(
    query: Query,
    usecase: Annotated[RAGQueryUseCase, Depends(get_rag_query_usecase)],
) -> QueryResult:
    """Execute a RAG query."""
    return await usecase.execute(query_text=query.text, top_k=query.top_k)
