# Architecture Overview

Zuko executes user-submitted code in an isolated Docker container and returns structured resource metrics.

## Component Diagram (Conceptual)

Request -> FastAPI Router -> Executor (orchestrator) -> FileManager -> DockerExecutor -> Docker Runtime
                                                   ↘ Models (validation) ↗

## Components

### API Layer (`main.py`, `zuko/api/routes.py`)

Receives JSON requests, validates via Pydantic, delegates to `run_code`.

### Executor (`zuko/core/executor.py`)

Simple dispatcher: validates language (currently only `python`) then coordinates file creation and sandbox execution.

### FileManager (`zuko/core/files.py`)

Context manager that writes the transient source and (optional) input to `/tmp`, returning host paths for mounting. Cleans up after execution.

### DockerExecutor (`zuko/core/sandbox.py`)

Runs the code inside a pre-built minimal image:

- Injects files via bind mount (`/tmp` -> `/app`)
- Applies isolation: no network, non-root, read-only FS, memory, CPU, PID caps
- Wraps execution with `/usr/bin/time -f "ZUKO_TIME:%U:%S ZUKO_MEMORY:%M"` to emit markers parseable post-run

### Models (`zuko/models/*.py`)

Provide typed interfaces for requests (`CodeRequest`) and responses (`ExecutionResult`). Future: unified `ExecutionResponse` wrapper & status enum.

## Execution Flow

1. Client POSTs code & optional input.
2. API validates request.
3. `run_code` checks language support.
4. `FileManager` writes temporary files in `/tmp`.
5. `DockerExecutor` starts container with constraints.
6. Container runs the script; `/usr/bin/time` outputs tagged metrics.
7. Logs captured; parser extracts CPU ms + peak RSS KB.
8. Temp files & container removed.
9. Structured `ExecutionResult` returned.

## Status Codes (Internal)

Currently used: `OK`, `RUNTIME_ERROR`, `TIMEOUT`, `ERROR`.

Planned mapping (enum proposal):

- OK – Successful execution (exit_code == 0)
- RUNTIME_ERROR – Non-zero exit code
- TIMEOUT – Container exceeded wall-clock limit
- ERROR – Infrastructure / unsupported language / unexpected failure

## Security Considerations

- Non-root user prevents privilege escalation
- Read-only root FS blocks writes (except mounted tmp dir)
- `no-new-privileges` forbids acquiring extra capabilities
- Network disabled avoids egress misuse
- PID / memory / CPU quotas mitigate resource exhaustion

Future hardening: seccomp / AppArmor profiles, syscall allow-listing, per-run ephemeral tmpfs, output size capping.

## Performance Notes

Current design spins a container per request (cold). Future optimizations:

- Reuse warm pool of paused containers (careful with isolation)
- Precompile for compiled languages (cache key: language + hash(source))
- Stream stdout for long-running outputs (bounded by timeouts)

## Extensibility Path

Add a language registry: `LANG_EXECUTORS = {"python": PythonExecutor, "cpp": CppExecutor}` each implementing `prepare()`, `run()`, `cleanup()`.

## Risks

- Docker daemon dependency – consider rootless mode
- Log parsing fragility – rely on tagged markers (already mitigated)
- Unbounded stdout/stderr – add size cap

## Glossary

- Peak RSS: Resident Set Size high-water mark (KB) from `/usr/bin/time %M`
- CPU Time: User + System seconds -> converted to ms

---
