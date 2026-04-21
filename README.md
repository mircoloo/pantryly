# Pantryly

Pantryly is a small FastAPI microservices stack for managing pantry products, user accounts, and JWT-based access through an Nginx gateway.

The repository currently runs three services in Docker Compose:

- `api-gateway`: the public entry point, exposed on port `8080`
- `auth-service`: user registration, login, token introspection, and JWT validation
- `inventory-service`: product CRUD, scoped to the authenticated user

There is also an `ai-service` in the repo, but it is not wired into the gateway or the default compose setup yet.

## Architecture

Requests go through the gateway first. Authentication is handled by `auth-service`, and `inventory-service` receives the authenticated user id in the `X-User-Id` header.

The gateway currently exposes these paths:

- `/api/v1/auth/*` and `/api/v1/users/*` -> `auth-service`
- `/api/v1/products/*` -> `inventory-service` after token introspection
- `/api/v1/ai` -> `503` for now

## Requirements

- Docker and Docker Compose
- For running services locally without Docker: Python 3.11+ and `uv`

## Setup

Create the environment files expected by the services:

`microservices/auth-service/.env`

```env
DATABASE_URL=sqlite:///./auth.db
JWT_SECRET=change-me
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

`microservices/inventory-service/.env`

```env
DATABASE_URL=sqlite:///./inventory.db
```

If you use PostgreSQL or another database, replace the SQLite URLs with your own connection strings.

## Run With Docker

From the repository root:

```bash
docker compose up --build
```

The gateway will be available at `http://localhost:8080`.

## API Notes

Auth endpoints exposed through the gateway include:

- `POST /api/v1/auth/login`
- `GET /api/v1/auth/introspect`
- `POST /api/v1/auth/verify_token`
- `POST /api/v1/users`
- `GET /api/v1/users`
- `GET /api/v1/users/me`

Inventory endpoints exposed through the gateway include:

- `POST /api/v1/products/products`
- `GET /api/v1/products/products`
- `GET /api/v1/products/products/{product_id}`
- `GET /api/v1/products/by-name/{product_name}`
- `GET /api/v1/products/by-barcode/{product_barcode}`
- `DELETE /api/v1/products/products/{product_id}`

Product requests require a bearer token. The gateway validates the token with `auth-service` and forwards the user id to inventory as `X-User-Id`.

## Service Scope

- `auth-service` owns users, password hashing, token generation, and token introspection.
- `inventory-service` stores products with `name`, `barcode`, and optional `expiration_date`.
- `ai-service` is intended for recipe generation, categorization, and chat, but it is still separate from the main compose flow.

## Repository Layout

```text
api-gateway/             Nginx reverse proxy
microservices/
  auth-service/          Authentication and user management
  inventory-service/     Product CRUD
  ai-service/            AI helpers and chat endpoints
```

## Development Notes

- Each service has its own FastAPI app and can be run independently during development.
- The inventory service uses the authenticated user id from the gateway; it does not trust client-supplied ownership data.
- The repo has service-level tests under `microservices/auth-service/tests` and `microservices/inventory-service/tests`.