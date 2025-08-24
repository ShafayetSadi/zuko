# Setup Guide

This guide brings a development instance of Zuko online locally.

## Prerequisites

- Docker (daemon running)
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## 1. Clone & Install

```bash
git clone <your-fork-or-origin> zuko
cd zuko
uv sync  # or: pip install -e .[dev]
```

## 2. Build Runtime Image

The executor expects an image tag `zuko-python:3.12`.

```bash
docker build -f docker/python.Dockerfile -t zuko-python:3.12 .
```

## 3. Run the API

```bash
uv run uvicorn main:app --reload
```

Open <http://127.0.0.1:8000/docs> for the interactive Swagger UI.

## 4. Execute a Snippet

```bash
curl -X POST http://127.0.0.1:8000/api/v1/execute \
  -H 'Content-Type: application/json' \
  -d '{"language":"python", "code":"print(1+2)"}'
```

## 5. Run Tests

```bash
uv run pytest -q
```

## 6. Lint (optional)

```bash
uv run ruff check .
```

## Troubleshooting

| Issue | Fix |
| ----- | --- |
| `Unsupported language` | Only `python` implemented today |
| `docker.errors.ImageNotFound` | Build the image (step 2) |
| `TIMEOUT` status | Increase `timeout` in request body |
| `permission denied` writing files | Ensure `/tmp` mount accessible to Docker |

## Next Steps

Explore architecture: `docs/architecture/overview.md` and consider contributing a new language backend.
