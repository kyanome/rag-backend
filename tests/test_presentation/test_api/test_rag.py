"""Tests for RAG API endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.presentation.api.app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_execute_rag_query(client: TestClient):
    """Test executing a RAG query."""
    response = client.post(
        "/api/rag/query",
        json={
            "text": "What is machine learning?",
            "top_k": 3,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["query"]["text"] == "What is machine learning?"
    assert data["query"]["top_k"] == 3
    assert "answer" in data
    assert isinstance(data["sources"], list)


def test_execute_rag_query_with_default_top_k(client: TestClient):
    """Test executing a RAG query with default top_k."""
    response = client.post(
        "/api/rag/query",
        json={
            "text": "Explain neural networks",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["query"]["top_k"] == 5  # Default value


def test_execute_rag_query_empty_text(client: TestClient):
    """Test executing a RAG query with empty text."""
    response = client.post(
        "/api/rag/query",
        json={
            "text": "",
            "top_k": 5,
        },
    )
    assert response.status_code == 422  # Validation error


def test_execute_rag_query_invalid_top_k(client: TestClient):
    """Test executing a RAG query with invalid top_k."""
    # top_k too low
    response = client.post(
        "/api/rag/query",
        json={
            "text": "Test query",
            "top_k": 0,
        },
    )
    assert response.status_code == 422

    # top_k too high
    response = client.post(
        "/api/rag/query",
        json={
            "text": "Test query",
            "top_k": 101,
        },
    )
    assert response.status_code == 422
