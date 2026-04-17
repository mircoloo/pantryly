# Pantryly - Auth Service

Welcome to the **Auth Service** for the Pantryly ecosystem!

This microservice is responsible for handling everything related to user identity, authentication, and authorization. We keep our users' data secure and provide reliable access tokens to let them interact securely with the rest of the Pantryly platform.

## What it does

- **User Registration & Management:** Create, update, and manage user accounts safely.
- **Authentication:** Validates user credentials and issues secure JSON Web Tokens (JWT).
- **Password Security:** Hashes and verifies passwords using modern cryptographic standards (`bcrypt` / `argon2`).
- **Authorization:** Grants appropriate access levels to users querying other Pantryly microservices.

## Tech Stack

We keep our stack modern, fast, and fully typed:

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Because it's amazingly fast and auto-generates our API docs)
- **Database:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Handles all our relational data mapping)
- **Token Management:** `PyJWT` and `python-jose` for verifying and signing tokens.
- **Data Validation & Settings:** [Pydantic V2](https://docs.pydantic.dev/) (Including `pydantic-settings` for robust environment variable management)
- **Dependency Management:** [`uv`](https://github.com/astral-sh/uv) (Extremely fast Python packaging)

## Project Structure

Here's a quick map to help you navigate the codebase:

```text
app/
├── api/v1/         # API Routers for authentication and user endpoints
├── core/           # Core configs, auth handlers, database setup, and logging
├── models/         # SQLAlchemy ORM models
├── repositories/   # Data access layer (abstracts DB operations)
├── schemas/        # Pydantic models for request/response validation
└── services/       # Business logic (kept separate from routers)
```

## Getting Started (Local Development)

Assuming you have Python 3.11+ and `uv` installed.

### 1. Setup the environment

Navigate to the `auth-service` directory and install dependencies:

```bash
cd microservices/auth-service
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file in the root of this service. Make sure to define the following essentials (check `app/core/config.py` for exact names):
```env
# Example .env configuration
DATABASE_URL=sqlite:///./auth.db  # Or your PostgreSQL connection string
SECRET_KEY=generate_a_strong_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Run the Service

Start the FastAPI application via Uvicorn:

```bash
uv run uvicorn app.main:app --reload
```

The service will start on `http://127.0.0.1:8000`. 
Head over to `http://127.0.0.1:8000/docs` to see the interactive Swagger UI!

## Running with Docker

If you prefer using Docker to run the entire stack (or just this service):

```bash
# From the auth-service folder
docker build -t pantryly-auth-service .
docker run -p 8000:8000 --env-file .env pantryly-auth-service
```
*(Note: It is usually recommended to run this alongside other services using the root `docker-compose.yml`.)*

## Testing

We use `pytest` for our testing suite. To execute the tests:

```bash
uv run pytest tests/
```

---
*Happy Coding! If you are adding features, please ensure your endpoints have proper validation schemas and your logic is tested.*