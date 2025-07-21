import pytest
from pydantic import ValidationError

from src.domain.rag.models.query import Query, QueryResult


class TestQuery:
    def test_create_query_with_defaults(self):
        query = Query(text="What is RAG?")

        assert query.text == "What is RAG?"
        assert query.top_k == 5

    def test_create_query_with_all_fields(self):
        query = Query(
            text="What is RAG?",
            top_k=10,
        )

        assert query.text == "What is RAG?"
        assert query.top_k == 10

    def test_empty_text_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            Query(text="")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("text",)
        assert "Query text cannot be empty" in errors[0]["msg"]

    def test_whitespace_text_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            Query(text="   ")

        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("text",)

    def test_text_stripped(self):
        query = Query(text="  What is RAG?  ")
        assert query.text == "What is RAG?"

    def test_top_k_validation(self):
        # Valid range
        query1 = Query(text="test", top_k=1)
        assert query1.top_k == 1

        query2 = Query(text="test", top_k=100)
        assert query2.top_k == 100

        # Invalid range
        with pytest.raises(ValidationError):
            Query(text="test", top_k=0)

        with pytest.raises(ValidationError):
            Query(text="test", top_k=101)


class TestQueryResult:
    def test_create_query_result(self):
        query = Query(text="What is RAG?")

        result = QueryResult(
            query=query,
            answer="RAG stands for Retrieval Augmented Generation...",
            sources=["doc1.pdf", "doc2.pdf"],
        )

        assert result.query == query
        assert result.answer == "RAG stands for Retrieval Augmented Generation..."
        assert result.sources == ["doc1.pdf", "doc2.pdf"]

    def test_create_query_result_with_defaults(self):
        query = Query(text="What is RAG?")

        result = QueryResult(
            query=query,
            answer="No information found.",
        )

        assert result.query == query
        assert result.answer == "No information found."
        assert result.sources == []
