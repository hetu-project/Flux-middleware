# Hetu Middleware

A FastAPI-based middleware service for the Hetu system.

## Features

- FastAPI for high-performance API
- SQLAlchemy for ORM
- Poetry for dependency management
- Alembic for database migrations
- Pydantic for data validation

## Development

### Setup

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run development server
uvicorn app.main:app --reload
```

### Project Structure

```
app/
├── api/          # API routes
├── core/         # Core configurations
├── crud/         # Database CRUD operations
├── db/           # Database configurations
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic models
└── services/     # Business logic
```
