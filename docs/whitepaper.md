# The Enterprise Agent OS

### A composite core that unifies AI, data, and agents on one resolvable model

**Technical Whitepaper · Agent DID / Fabric of Work**

---

## Summary

Enterprises are deploying autonomous agents faster than they can govern them.
Today that means stitching together a vector database for memory, an identity
system for the agent, a graph database for relationships, a policy engine for
authorization, and a benchmark harness for evaluation — five systems, five trust
boundaries, no shared notion of what is *true*, *valid*, or *trusted*.

We take a different position: **AI, data, and agents are one model, not three.**
The Fabric of Work is a single self‑describing graph in which everything — a
record, a memory, a credential, a policy, an agent, even the schema itself — is a
**box**: data placed in a context. A system is **real** when every reference
resolves and **stable** when every box is typed, filled, and placed. The same
check validates the database, the AI memory, and the agent's trust — at once.

To our knowledge this is the **first composite AI + DB + agent core** published
as one resolvable, governable, trust‑scored model — an **Enterprise Agent OS**.

---

## The problem: a fragmented stack has no shared truth

| Layer | Typical tool | What it can't do alone |
|---|---|---|
| Memory / RAG | vector DB | doesn't know who an agent is, or whether a memory is trusted |
| Identity | Okta / SCIM | doesn't store or retrieve agent memory |
| Relationships | graph DB | doesn't score trust or detect drift |
| Authorization | policy engine | separate from the data it governs |
| Evaluation | benchmark harness | sits outside the system it measures |

Each tool optimizes one workload and owns its own truth. The seams between them
are where agents drift, leak, and fail — and where governance has nothing to hold.

## The thesis: data‑in‑context, resolved

A datum has no intrinsic meaning or value; the same number is useless in one
context and decisive in another. The fabric makes this literal:

- **Box** — data in a context (a record, memory, credential, policy, agent…).
- **Kind** — a class; **relation** — a typed edge; **context** — a scope. Each is
  itself a box, so the *model lives in the graph*, bottoming out in a self‑typed
  fixpoint (`kind:kind`).
- **Resolution** — *node → real* (every reference resolves) and *box → stable*
  (every box typed, filled, placed). Validity is **computed, not assumed**.

Because the model is one kind of thing, one check governs everything. A memory, an
identity, and a policy are all boxes that must resolve.

## The composite core

```
            ┌──────────────────────────────────────────────┐
            │              ENTERPRISE AGENT OS               │
            │   one self-describing graph · node+box resolve │
            ├───────────────┬───────────────┬───────────────┤
            │   AI layer     │   DB layer    │  Agent layer  │
            │ memory · RAG · │ boxes-in-ctx ·│ identity ·    │
            │ scoring        │ graph · HTAP  │ governance ·  │
            │                │               │ trust         │
            └───────────────┴───────────────┴───────────────┘
                     the SAME resolution validates all three
```

- **AI** — retrieval is context‑scoped (faster *and* more accurate), memory is
  bi‑temporal (`as_of` time T), and every answer is restricted to **trusted,
  resolved** boxes — drift‑resistant by construction.
- **DB** — a graph store that is transactional and analytical (HTAP) on the same
  boxes; schemaless where you need flexibility, never structureless.
- **Agent** — identity is a box, authorization is a relationship (ReBAC), trust is
  a **computed score** (GPA + risk/threat), and meaning is governed by reasoned,
  federated procedure rather than decree.

## What makes it different: the contract is ours

The **contract** — the box model, the resolution invariant, the trust and
governance rules — is owned by the platform. A database does not define it; it
**conforms** to it. The store is therefore a **feature** we embed (open‑source,
in‑process, edge, air‑gappable), not a **provider** that owns us. Vendor‑neutrality
isn't aspirational here — it's structural: any engine that satisfies the contract
is interchangeable.

We turn that into a measurement — a **Platform Benchmark**: engines are scored by
how well they host our contract, not by which one locks us in. We build on
**SurrealDB**, which conforms most closely and is production‑proven at enterprise
scale (e.g., Samsung), while remaining swappable for Neo4j, ArangoDB, Postgres,
and others.

## Proof: reproducible, in one command

Every number regenerates with `bash scripts/run_benchmarks.sh` (deterministic,
offline). A Rust core (`crates/fabric-core`) and a Python reference both implement
the same resolution.

| Property | Result |
|---|---|
| Constitution + model | resolve at node + box → **VALID (real + stable)** |
| Resolution throughput | **~23.5M elements/s/core**, linear; 8×10⁹ as ~160 federated shards |
| Retrieval | context‑scoped memory **3.7× faster** than global RAG at **100%** precision |
| Agent quality | Trust/Reliability/Usability → **GPA + risk/threat** (drift‑resistant) |
| Resilience (chaos) | random 10% kill → 66%; **shard kill → 92–98%** intact |
| HTAP | **1.8M ops/s** OLTP + **2.9M rows/s** OLAP on one graph |
| Fraud detection | laundering rings + velocity + anomaly + untrusted — all caught |

## Enterprise‑ready by construction

- **Brings your schema unchanged** — Adobe XDM, Salesforce, Okta/SCIM map onto
  boxes‑in‑context and resolve (FHIR, FIBO, schema.org follow the same pattern).
- **Maps to security frameworks** — OWASP Top 10 for LLM Apps and CSA AICM/STAR;
  authorization via OpenFGA as pure relationship data.
- **Multi‑tenant, ACID, real‑time, air‑gappable** — from a laptop to a sealed
  facility; the most secure agent is local memory + local model + zero ingress.

## Vision: the Internet of Agents

At scale, federation *is* the Internet of Agents — a network for **work**, not
pages, where agents join by adopting the contract rather than registering with a
central authority. The platform is the meaning‑and‑trust layer that outlives any
vendor, cloud, or model.

---

*Reproduce:* `bash scripts/run_benchmarks.sh` · *Core:* `crates/fabric-core`
(Rust), `scripts/fabric_*.py` (reference) · *Spec:* `docs/fabric-of-work.md` ·
*Paper:* `docs/fabric-paper.md` · *Benchmarks:* `docs/BENCHMARKS.md`.
