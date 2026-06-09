# Contributing to Agent OS

Thanks for your interest — contribution is permissionless and welcome.

## Ground rules

- Be respectful; follow the [Code of Conduct](./CODE_OF_CONDUCT.md).
- Discuss significant changes in an issue first.
- Keep PRs focused; include tests and update docs.

## Developer Certificate of Origin (DCO)

All commits must be signed off, certifying you have the right to submit them under
the project's license (the [DCO](https://developercertificate.org/)):

```bash
git commit -s -m "your message"
```

This adds a `Signed-off-by: Your Name <you@example.com>` trailer. PRs without DCO
sign‑off cannot be merged.

## Development

```bash
# Rust core
cargo test -p fabric-core

# Reference + benchmarks (no external deps, deterministic)
bash scripts/run_benchmarks.sh

# Containerized
docker build -f deploy/fabric/Dockerfile -t agent-os:local .
```

The bar for merge: the graph still **resolves at node + box** (real + stable),
tests pass, and benchmarks reproduce.

## Pull requests

1. Fork and branch.
2. Make the change; add tests; sign off (`-s`).
3. Open a PR describing the *why*. A maintainer will review under the
   [governance](./GOVERNANCE.md) process (reasoned review; objections must carry
   reasons).

## Reporting security issues

Do **not** open public issues for vulnerabilities — see [SECURITY.md](./SECURITY.md).
