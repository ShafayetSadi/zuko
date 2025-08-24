# Zuko

A scalable, sandboxed code execution engine

---

Zuko executes untrusted user code inside an isolated Docker container and reports CPU time and peak RSS memory similar to coding contest platforms.

## Features (v0.1.0)

- FastAPI API: POST `/api/v1/execute`
- Python 3.12 sandbox (non-root, read-only FS, no network, pids/memory/CPU limits)
- Deterministic resource measurement via `/usr/bin/time`
- Temporary file management with automatic cleanup
- Structured results (`status`, `stdout`, `stderr`, `time_used_ms`, `memory_used_kb`)
- Test suite (pytest) for core behavior

## Example

Request:

```json
POST /api/v1/execute
{
  "language": "python",
  "code": "name = input()\nprint(f'Hello {name}')",
  "input_data": "Zuko"
}
```

Response:

```json
{
  "status": "OK",
  "stdout": "Hello Zuko\n",
  "stderr": "",
  "exit_code": 0,
  "time_used": 12.4,
  "memory_used": 10240
}
```

## Safety Controls

- `read_only` container FS + mounted temp dir
- `network_disabled=true`
- Non-root `runner` user
- `pids_limit=64` / `mem_limit=128m` / `nano_cpus=1_000_000_000`
- `no-new-privileges` security opt

## Architecture (High level)

| Layer   | Components                                | Responsibility                                       |
| ------- | ----------------------------------------- | ---------------------------------------------------- |
| API     | FastAPI app, `routes.py`                  | Accept execution requests                            |
| Core    | `executor.py`, `files.py`, `sandbox.py`   | Orchestrate, manage temp files, run Docker container |
| Sandbox | Docker image (`docker/python.Dockerfile`) | Constrained runtime & measurement                    |
| Models  | Pydantic request/response models          | Validation & shaping IO                              |
| Tests   | `tests/`                                  | Regression safety                                    |

See `docs/architecture/overview.md` for more detail.

## Quick Start (Dev)

Prereqs: Docker, Python 3.12+, uv (or pip)

```bash
# Install deps
uv sync 

# Build runtime image (needed for execution)
docker build -f docker/python.Dockerfile -t zuko-python:3.12 .

# Run API
uv run uvicorn main:app --reload

# Test
uv run pytest -q
```

## API Contract

Endpoint: `POST /api/v1/execute`

| Field      | Type   | Notes                                        |
| ---------- | ------ | -------------------------------------------- |
| language   | string | Must be `python` (others return `ERROR`)     |
| code       | string | Required source code                         |
| input_data | string | Optional stdin contents                      |
| timeout    | int    | Seconds (default 3) – container wait timeout |

Statuses currently emitted: `OK`, `RUNTIME_ERROR`, `TIMEOUT`, `ERROR`.

## Roadmap (Excerpt)

Planned: multi-language (C++/GCC, Java), multi-testcase orchestration, contest / scoring layer. Full list: `docs/roadmap.md`.

## Contributing

1. Fork & branch
2. Add / update tests
3. Run lint + tests
4. Follow Conventional Commits (`feat:`, `fix:`, etc.)

## License

MIT – see `LICENSE`.

## FAQ

**Why Python 3.12?** The runtime container & local dev target the same minor version for determinism.

**Why not Firecracker / WASI?** Early stage—Docker offers quickest iteration. Future isolation layers are possible.

---

For detailed docs visit `docs/index.md`.
