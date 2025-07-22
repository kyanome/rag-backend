# RAG Backend

Retrieval-Augmented Generation (RAG) backend service built with FastAPI and Azure OpenAI.

## Features

- **FastAPI** for high-performance async REST API
- **Azure OpenAI** integration for intelligent responses
- **Document Management** with CRUD operations
- **RAG Query Engine** for context-aware Q&A
- **Clean Architecture** for maintainability and testability
- **Azure AD Authentication** using DefaultAzureCredential
- **Type Safety** with Pydantic and strict mypy
- **Comprehensive Testing** with pytest

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Azure subscription with OpenAI service
- Azure CLI (for authentication)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/rag-backend.git
cd rag-backend
```

2. Install dependencies using uv:

```bash
uv sync
```

3. Set up Azure authentication:

```bash
az login
```

4. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your Azure OpenAI details
```

## Configuration

Create a `.env` file with the following variables:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT=your-chat-deployment-name
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your-embedding-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-01

# Azure Cognitive Search Configuration (optional)
AZURE_SEARCH_ENDPOINT=https://your-resource.search.windows.net
AZURE_SEARCH_INDEX_NAME=documents

# RAG Strategy
RAG_STRATEGY=simple  # Options: simple, mock (for testing)
```

To find your deployment names:

```bash
az cognitiveservices account deployment list \
  --name <your-openai-resource-name> \
  --resource-group <your-resource-group>
```

## Usage

### Starting the Server

```bash
uv run python main.py
```

The API will be available at `http://localhost:8010`

### API Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8010/docs`
- ReDoc: `http://localhost:8010/redoc`

### Example API Calls

#### Health Check

```bash
curl http://localhost:8010/health
```

#### Add a Document

```bash
curl -X POST http://localhost:8010/api/documents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to AI",
    "content": "Artificial Intelligence is the simulation of human intelligence...",
    "source": "AI Handbook"
  }'
```

#### List Documents

```bash
curl http://localhost:8010/api/documents
```

#### Execute RAG Query

```bash
curl -X POST http://localhost:8010/api/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is artificial intelligence?",
    "top_k": 5
  }'
```

## Development

### Code Quality

Run all checks:

```bash
make check
```

Individual commands:

```bash
make lint       # Run linter
make format     # Format code
make typecheck  # Type checking
```

### Testing

Run all tests:

```bash
make test
```

Run specific tests:

```bash
uv run pytest tests/test_domain/
uv run pytest -k "test_document"
```

### Local Development without Azure

For local development without Azure credentials:

```bash
export RAG_STRATEGY=mock
uv run python main.py
```

## Architecture

The project follows Clean Architecture principles:

```
src/
├── domain/         # Business logic and entities
├── infrastructure/ # External service implementations
├── usecase/        # Application services
└── presentation/   # REST API layer
```

Key patterns:

- **Repository Pattern** for data abstraction
- **Strategy Pattern** for RAG algorithms
- **Dependency Injection** for loose coupling

### Current Implementation Status

- **Document Storage**: In-memory repository (production implementation pending)
- **Search Strategy**: Simple retrieval of recent documents (Azure Cognitive Search integration pending)
- **RAG Strategy**:
  - `SimpleRAGStrategy`: Returns all documents without semantic search
  - `MockRAGStrategy`: For testing without Azure dependencies

Future enhancements will include:

- Azure Cognitive Search for semantic document retrieval
- Persistent document storage (e.g., Azure Cosmos DB)
- Advanced RAG strategies with embedding-based search

## API Endpoints

| Method | Endpoint                       | Description           |
| ------ | ------------------------------ | --------------------- |
| GET    | `/health`                      | Health check          |
| GET    | `/api/documents`               | List all documents    |
| GET    | `/api/documents/{document_id}` | Get specific document |
| POST   | `/api/documents`               | Create new document   |
| PUT    | `/api/documents/{document_id}` | Update document       |
| DELETE | `/api/documents/{document_id}` | Delete document       |
| POST   | `/api/rag/query`               | Execute RAG query     |

## License

This project is licensed under the MIT License - see the LICENSE file for details.
