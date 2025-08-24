# Changelog

All notable changes to **Zuko** will be documented in this file.  
This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and uses [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

- Add C++ and Java language support
- Implement multi-testcase execution
- Contest system integration (future)
- Replace ad-hoc status strings with enum
- Add CI workflow

---

## [0.1.0] – 2025-08-24

### Added

- **Core Execution Engine (Python only)**

  - Runs Python code inside Docker containers.
  - Enforces CPU, memory, and process limits.
  - Sandboxes execution (no network, read-only FS, no new privileges).

- **Accurate Time & Memory Measurement**

  - Integrated `/usr/bin/time` for Codeforces-like reporting.
  - Reports CPU time (user + system) in ms.
  - Reports peak memory (RSS) in KB.

- **Custom Python Runtime Image**

  - Built `zuko-python:3.12` with `time` pre-installed.
  - Runs as non-root user for security.

- **Testing Infrastructure**

  - Added stress tests (CPU-heavy, memory-heavy, I/O, error, timeout).
  - Verified results match Codeforces-style reporting.

- **Documentation Setup**
  - Created `docs/progress/` for weekly devlogs.
  - Added `CHANGELOG.md` for milestone tracking.
  - Adopted Conventional Commits for clean history.

---

## Versioning Notes

- `0.x` = Early development (breaking changes expected).
- `1.0.0` = Stable release (after multi-language + contest features).

---
