"""FastAPI application setup."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.api.routes import documents, rag  # type: ignore[attr-defined]


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="RAG Backend API",
        description="Retrieval-Augmented Generation backend service",
        version="0.1.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure based on your needs
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
    app.include_router(rag.router, prefix="/api/rag", tags=["RAG"])

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy"}

    return app
