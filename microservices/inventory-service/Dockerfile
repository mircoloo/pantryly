FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.2 /uv /uvx /bin/

WORKDIR /usr/src/app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY . .

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
