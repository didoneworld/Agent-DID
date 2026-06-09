# Security Policy

## Reporting a vulnerability

Please report security vulnerabilities **privately**. Do not open a public issue.

- Use GitHub's **private vulnerability reporting** (Security → Report a
  vulnerability) on this repository, or
- email the maintainers (see [`MAINTAINERS.md`](./MAINTAINERS.md)).

Include a description, reproduction steps, affected versions, and any known
mitigations. We aim to acknowledge within 3 business days and to coordinate a fix
and disclosure timeline with you.

## Scope

Agent OS is designed for a **minimal attack surface** — one box type,
context‑enforced access, no out‑of‑band schema engine, and an air‑gappable
deployment profile. Its security model maps to the OWASP Top 10 for LLM
Applications and CSA AICM/STAR; see `docs/fabric-security.md`.

## Supported versions

Until a 1.0 release, security fixes target the `main` branch. Tagged releases will
carry a supported‑versions table here.

## Coordinated disclosure

We follow coordinated disclosure: we will not disclose a reported issue publicly
until a fix is available, and we will credit reporters who wish to be credited.
