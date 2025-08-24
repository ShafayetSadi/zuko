# Roadmap

This roadmap is intentionally lightweight; items may shift as feedback arrives.

## Legend

- [x] Done | [ ] Planned | (R) Research / spike phase

## Milestones

### 0.1.x – Foundational Sandbox

- [x] Python execution (Docker, constrained)
- [x] Resource measurement (time + peak RSS)
- [x] Basic API endpoint `/api/v1/execute`
- [x] Minimal test coverage

### 0.2.x – Robustness & DX

- [ ] Add status enum + richer error taxonomy
- [ ] Improve logging / tracing (structured logs)
- [ ] Add CI workflow (lint + tests + image build)
- [ ] Add simple rate limiting (middleware) (R)

### 0.3.x – Multi-Language

- [ ] C++ (GCC) toolchain image
- [ ] Java (JDK 21) image
- [ ] Language selection dispatch layer
- [ ] Compilation caching (optional)

### 0.4.x – Testcase Orchestration

- [ ] Multi-testcase input execution
- [ ] Aggregate scoring + per-test breakdown
- [ ] JSON schema for batch executions

### 0.5.x – Contest Primitives

- [ ] Problem model & metadata ingestion
- [ ] Submission model + persistence (SQLite/Postgres)
- [ ] Leaderboard & scoring rules

### 0.6.x – Scale & Security Hardening

- [ ] Worker pool abstraction (async queue)
- [ ] Metrics / Prometheus endpoints
- [ ] Enhanced sandboxing (seccomp / AppArmor profiles) (R)
- [ ] Optional Firecracker / WASI evaluation (R)

### 1.0.0 – Stable

- [ ] Public API docs & OpenAPI examples
- [ ] SLA & versioning policy
- [ ] Hard multi-language guarantees

## Stretch / Ideas

- [ ] Web UI playground
- [ ] Pluggable scoring strategies
- [ ] Source code static analysis (basic heuristics)

## Recently Completed

See `changelog.md` for versioned detail.
