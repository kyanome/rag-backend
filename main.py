"""Main entry point for the RAG backend application."""

import uvicorn

from src.presentation.api.app import create_app


def main() -> None:
    """Run the FastAPI application."""
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
