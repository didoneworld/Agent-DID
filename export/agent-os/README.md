<div align="center">

# Agent OS

### The Enterprise Agent OS — one resolvable core for AI, data, and agents.

</div>

Enterprises are shipping autonomous agents faster than they can govern them.
Today that means stitching together a vector database for memory, an identity
system for the agent, a graph database for relationships, a policy engine for
authorization, and a benchmark harness for evaluation — **five systems, five trust
boundaries, no shared notion of what is true, valid, or trusted.**

**Agent OS takes a different position: AI, data, and agents are one model, not
three.** Everything — a record, a memory, a credential, a policy, an agent, even
the schema itself — is a **box**: data placed in a context. A system is **real**
when every reference resolves and **stable** when every box is typed, filled, and
placed. The *same* check validates the database, the AI memory, and the agent's
trust — at once.

To our knowledge this is the **first composite AI + DB + agent core** published as
one resolvable, governable, trust‑scored model.

---

## The composite core

```
            ┌──────────────────────────────────────────────┐
            │                  AGENT OS                       │
            │   one self-describing graph · node+box resolve  │
            ├───────────────┬───────────────┬────────────────┤
            │   AI layer     │   DB layer    │   Agent layer  │
            │ memory · RAG · │ boxes-in-ctx ·│ identity ·     │
            │ scoring        │ graph · HTAP  │ governance ·   │
            │                │               │ trust          │
            └───────────────┴───────────────┴────────────────┘
                     the SAME resolution validates all three
```

- **AI** — context‑scoped retrieval (faster *and* more accurate), bi‑temporal
  memory (`as_of` time T), answers restricted to **trusted, resolved** boxes —
  drift‑resistant by construction.
- **DB** — a graph store that is transactional *and* analytical (HTAP) on the same
  boxes; schemaless where you need it, never structureless.
- **Agent** — identity is a box, authorization is a relationship (ReBAC/OpenFGA),
  trust is a **computed score** (GPA + risk/threat), and meaning is governed by
  reasoned, federated procedure — not decree.

## Why it's different: the contract is ours

The **contract** — the box model, the resolution invariant, the trust and
governance rules — is owned by the platform. A database doesn't define it; it
**conforms** to it. The store is a **feature** we embed (open‑source, in‑process,
edge, air‑gappable), not a **provider** that owns us. Vendor‑neutrality is
structural: any engine that satisfies the contract is interchangeable. We measure
this directly with a **Platform Benchmark** (contract conformance), and build on
**SurrealDB** — production‑proven at enterprise scale (e.g., Samsung) and the
closest fit — while remaining swappable for Neo4j, ArangoDB, Postgres, and more.

## Proof — reproducible, in one command

| Property | Result |
|---|---|
| Constitution + model | resolve at node + box → **VALID (real + stable)** |
| Resolution throughput | **~23.5M elements/s/core**, linear; 8×10⁹ as ~160 federated shards |
| Retrieval | context‑scoped memory **3.7× faster** than global RAG at **100%** precision |
| Agent quality | Trust/Reliability/Usability → **GPA + risk/threat** (drift‑resistant) |
| Resilience (chaos) | random 10% kill → 66%; **shard kill → 92–98%** intact |
| HTAP | **1.8M ops/s** OLTP + **2.9M rows/s** OLAP on one graph |
| Fraud detection | laundering rings + velocity + anomaly + untrusted — all caught |

```bash
bash scripts/run_benchmarks.sh        # deterministic, offline
cargo run -p fabric-core              # the Rust core resolves the kernel
```

## Enterprise‑ready by construction

- **Brings your schema unchanged** — Adobe XDM, Salesforce, Okta/SCIM (and FHIR,
  FIBO, schema.org) map onto boxes‑in‑context and resolve.
- **Maps to security frameworks** — OWASP Top 10 for LLM Apps, CSA AICM/STAR;
  authorization via OpenFGA as pure relationship data.
- **Multi‑tenant, ACID, real‑time, air‑gappable** — from a laptop to a sealed
  facility; the most secure agent is local memory + local model + zero ingress.

## Architecture & ecosystem

| Repo | Role |
|---|---|
| **Agent OS** (this) | the Enterprise Agent OS — the composite core |
| [Agent DID](https://github.com/didoneworld/agent-did) | identity control plane + the Fabric of Work spec, reference impl, Rust core, benchmarks |
| [AGenNext/Agent‑Bench](https://github.com/AGenNext/Agent-Bench) | SWE‑bench‑style agent benchmark layer (Rust + SurrealQL) |

## Quick start

```bash
# Rust core (Rust + SurrealQL stack)
cargo test -p fabric-core

# Reference + benchmarks (no deps)
bash scripts/run_benchmarks.sh

# Containerized
docker build -f deploy/fabric/Dockerfile -t agent-os:local .
docker run --rm agent-os:local

# On Kubernetes (KinD)
bash deploy/publish-kind.sh
```

## Documentation

- **Whitepaper** — the Enterprise Agent OS, for builders and buyers
- **Technical paper** — model, resolution criterion, benchmarks, limitations
- **The constitution** — the structured instruction set governing meaning, work,
  and trust
- **Benchmarks** — public, deterministic results

## Vision: the Internet of Agents

At scale, federation *is* the Internet of Agents — a network for **work**, not
pages, where agents join by adopting the contract rather than registering with a
central authority. The platform is the meaning‑and‑trust layer that outlives any
vendor, cloud, or model.

## Governance & licensing

Agent OS is **vendor‑agnostic by design** and built for open, foundation‑style
stewardship:

- **Apache‑2.0** licensed ([`LICENSE`](./LICENSE)) — permissive, foundation‑ready.
- **Open governance** ([`GOVERNANCE.md`](./GOVERNANCE.md)) — meritocratic
  maintainership, public decision‑making, no single‑vendor control. *Meaning is
  derived, not decreed* — the same principle governs the project.
- **DCO sign‑off** on contributions ([`CONTRIBUTING.md`](./CONTRIBUTING.md)),
  Contributor Covenant ([`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)), coordinated
  disclosure ([`SECURITY.md`](./SECURITY.md)), and named
  [`MAINTAINERS.md`](./MAINTAINERS.md).
- **No vendor lock‑in** — the contract is the project's, the substrate is a
  swappable feature; nothing here depends on a single cloud or database vendor.

---

<div align="center">
<sub>Open core · vendor‑agnostic by contract · Apache‑2.0 · Rust + SurrealQL</sub>
</div>
