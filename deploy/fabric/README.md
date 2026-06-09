# Containerized fabric core

A self-contained image of the Enterprise Agent OS core: the **Rust `fabric-core`**
binary, the **Python reference + benchmarks**, the **SurrealQL** schema, and the
**spec**. On start it proves the core resolves, then runs the deterministic
benchmark suite.

## Build & run

```bash
# from the repo root
docker build -f deploy/fabric/Dockerfile -t fabric-core:local .
docker run --rm fabric-core:local
```

Or with a live SurrealDB alongside:

```bash
docker compose -f deploy/fabric/compose.yml up --build
```

## What's inside

| Layer | Path |
|---|---|
| Rust core (built + tested) | `/usr/local/bin/fabric-core` |
| Python reference + benchmarks | `/fabric/scripts/` |
| SurrealQL backend | `/fabric/experiments/fabric/` |
| Spec + benchmarks docs | `/fabric/docs/` |

Default `CMD`: `fabric-core && bash scripts/run_benchmarks.sh` — exits non-zero if
the core does not resolve (real + stable), so the image doubles as a CI gate.
