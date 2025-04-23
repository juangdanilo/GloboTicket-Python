# REST API with FastApi and SQLAlchemy as ORM

Globoticket is a REST API built with Python 3 and FastAPI for managing event listings and ticket purchases. This project includes a SQL database backend, API endpoints for event management, and a web frontend for user interaction.

## Features

- **RESTful API** with FastAPI
- SQLite database with SQLAlchemy ORM
- Automatic API documentation (Swagger UI/OpenAPI)
- Web frontend with dynamic content loading
- Pre-configured testing environment with pytest
- Pre-commit hooks for code quality checks

## Database Schema

### Tables
```sql
CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE event (
    id INTEGER PRIMARY KEY,
    product_code VARCHAR NOT NULL UNIQUE,
    date DATE NOT NULL,
    price NUMERIC NOT NULL,
    category_id INTEGER NOT NULL REFERENCES category(id)
);
```

## Installation

### Prerequisites

- Python 3.12+
- Poetry package manager

### Setup

1) Clone the repository
2) Install dependencies:

```bash
poetry install
```

## Usage

### Start the server

```bash
poetry run python runserver.py
```

The API will be available at:

- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Frontend: http://localhost:8000

## API Endpoints

| Endpoint      | Method | Description            |
| ------------- | ------ | ---------------------- |
| `/event/{id}` | GET    | Get single event by ID |
| `/event/`     | GET    | Get all events         |

## Testing

Run tests with:
```bash
poetry run pytest
```
Test coverage includes:

- API endpoint validation
- Database operations
- Error handling

## Frontend Features

- Catalog view of all events
- Event detail pages
- Dynamic content loading via AJAX

## Development Tools

- Pre-commit hooks for:
  - Black code formatting
  - Flake8 linting
  - mypy type checking
  - isort import sorting
  - SQLAlchemy ORM
  - pytest with test database fixtures

## License

This project is released under The Unlicense - free for any use.