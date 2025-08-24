# Zuko Docs

An experimental, sandboxed code execution engine – Python first, extensible for future languages.

## Start Here

1. Read the [Setup Guide](guides/setup.md) to get the API running.
2. Review the [Architecture Overview](architecture/overview.md) to understand components.
3. Check the [Roadmap](roadmap.md) & [Changelog](changelog.md) for status.

## Structure

| Section | Purpose |
|---------|---------|
| `architecture/` | Design, security, component diagrams |
| `guides/` | How-to & setup instructions |
| `progress/` | Time-stamped development logs |
| `roadmap.md` | Forward-looking milestones |
| `changelog.md` | Versioned changes (Keep a Changelog) |

## Core Concepts

- Deterministic resource measurement via `/usr/bin/time` wrapper tokens.
- Sandboxed Docker runtime with strict limits.
- Stateless API: each execution is isolated.
- Extensible executor abstraction (future multi-language backends).

> Missing something? Open an issue or PR—docs are a living contract.
