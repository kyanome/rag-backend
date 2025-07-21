"""Tests for document API endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.presentation.api.app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_create_document(client: TestClient):
    """Test creating a document."""
    response = client.post(
        "/api/documents",
        json={
            "title": "Test Document",
            "content": "Test content",
            "source": "test.txt",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Document"
    assert data["content"] == "Test content"
    assert data["source"] == "test.txt"
    assert "id" in data


def test_get_document(client: TestClient):
    """Test getting a document by ID."""
    # Create a document
    create_response = client.post(
        "/api/documents",
        json={
            "title": "Test Document",
            "content": "Test content",
        },
    )
    document_id = create_response.json()["id"]

    # Get the document
    response = client.get(f"/api/documents/{document_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == document_id
    assert data["title"] == "Test Document"


def test_get_nonexistent_document(client: TestClient):
    """Test getting a nonexistent document."""
    response = client.get("/api/documents/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_list_documents(client: TestClient):
    """Test listing documents."""
    # Create multiple documents
    for i in range(3):
        client.post(
            "/api/documents",
            json={
                "title": f"Document {i}",
                "content": f"Content {i}",
            },
        )

    # List documents
    response = client.get("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert len(data["documents"]) >= 3
    assert data["total"] >= 3


def test_list_documents_with_pagination(client: TestClient):
    """Test listing documents with pagination."""
    # Clear existing documents first
    client.delete("/api/documents")

    # Create 5 documents
    for i in range(5):
        client.post(
            "/api/documents",
            json={
                "title": f"Document {i}",
                "content": f"Content {i}",
            },
        )

    # Get first 2 documents
    response = client.get("/api/documents?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["documents"]) == 2


def test_update_document(client: TestClient):
    """Test updating a document."""
    # Create a document
    create_response = client.post(
        "/api/documents",
        json={
            "title": "Original Title",
            "content": "Original content",
        },
    )
    document_id = create_response.json()["id"]

    # Update the document
    response = client.put(
        f"/api/documents/{document_id}",
        json={"content": "Updated content"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated content"
    assert data["title"] == "Original Title"  # Title unchanged


def test_update_nonexistent_document(client: TestClient):
    """Test updating a nonexistent document."""
    response = client.put(
        "/api/documents/00000000-0000-0000-0000-000000000000",
        json={"content": "New content"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_delete_document(client: TestClient):
    """Test deleting a document."""
    # Create a document
    create_response = client.post(
        "/api/documents",
        json={
            "title": "To Delete",
            "content": "Will be deleted",
        },
    )
    document_id = create_response.json()["id"]

    # Delete the document
    response = client.delete(f"/api/documents/{document_id}")
    assert response.status_code == 200
    assert response.json()["deleted"] is True

    # Verify it's deleted
    get_response = client.get(f"/api/documents/{document_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_document(client: TestClient):
    """Test deleting a nonexistent document."""
    response = client.delete("/api/documents/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_delete_all_documents(client: TestClient):
    """Test deleting all documents."""
    # Create multiple documents
    for i in range(3):
        client.post(
            "/api/documents",
            json={
                "title": f"Document {i}",
                "content": f"Content {i}",
            },
        )

    # Delete all
    response = client.delete("/api/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["deleted_count"] >= 3

    # Verify all are deleted
    list_response = client.get("/api/documents")
    assert list_response.json()["documents"] == []
