# The Fabric of Work: A Self-Describing, Resolvable Graph Substrate for Governed Agentic Work

**Status:** Working paper / preprint draft. Reproducible; derived and contestable
(`fabric-of-work.md` §12). All result numbers regenerate via
`bash scripts/run_benchmarks.sh`; full results in `docs/BENCHMARKS.md`.
Companion analyses: `fabric-substrate-comparison.md` (substrates + blockchain),
`fabric-security.md` (OWASP/CSA), `fabric-bleeding-edge.md` (temporal KGs),
`fabric-swot.md` (SWOT + cost + chaos).

## Abstract

We present **the Fabric of Work**, a substrate for governed agentic work in which
all entities — data, agents, schemas, and the model itself — are uniform **boxes**
(nodes) carrying *data-in-context*, related by edges in a graph. We define a
two-level validity criterion: a system is **real** if its reference graph resolves
at every **node** (no dangling references) and **stable** if every node, treated
as a **box**, is filled, placed in a context-slot, and typed. The model is
**self-describing**: its metamodel (kinds, relations) lives in the graph as boxes,
terminating in a self-typed fixpoint (`kind:kind`). We give a reference
implementation and four reproducible benchmarks showing (i) graph resolution is
linear at ~23.5M elements/s/core and reaches 8×10⁹ boxes as a federation of ~160
shards; (ii) context-scoped retrieval is ~3.7× faster than global vector search at
equal precision; (iii) agent quality (Trust, Reliability, Usability, a composite
GPA, and a risk/threat profile) is computable from provenance-bearing data. We
evaluate three storage substrates (SurrealDB, SpacetimeDB, PostgreSQL) and argue
SurrealDB matches the model's requirements, with SpacetimeDB's fused
backend/runtime as a deliberate non-fit. We validate the model against six use
cases (context store, feature store, AI registry, agent marketplace, lifecycle
management, cross-framework benchmarking).

## 1. Introduction

Autonomous agents increasingly **construct work** over real and digital things.
Such work must be *continuous, durable, measurable, governable, and value-
generating*, and its meaning must be legitimately established rather than decreed.
We formalize meaning as **data-in-context**: the same datum is useless or
invaluable depending on context. The contribution is a minimal model in which
governance, scale, retrieval, and trust are all expressed and *checked* uniformly.

**Contributions.** (1) A self-describing box/context graph model and a node+box
resolution criterion (§2). (2) A reference resolver and a homoiconic stable-state
model (§3). (3) Reproducible benchmarks for scale, retrieval (RAG/memory/trust),
and agent scoring (§4). (4) A substrate evaluation (§5) and use-case validation
(§6).

**Novelty (positioning).** To our knowledge, this is the **first published
platform to unify an AI + DB + agent composite core** on a single self-describing,
resolvable model — where the *same* node+box resolution validates **data** (the DB
layer), **memory/RAG/scoring** (the AI layer), and **identity/governance/trust**
(the agent layer) alike. Equivalently, the composite core **is an Enterprise Agent
OS**, and this work **benchmarks the Enterprise Agent OS** end to end (resolution,
retrieval, scoring, chaos/resilience, HTAP, and a contract-conformance *Platform
Benchmark*). It is *enterprise* in the concrete sense that it hosts existing
enterprise data models unchanged (Adobe XDM, Salesforce, Okta/SCIM — §6),
maps to enterprise security/compliance frameworks (OWASP LLM Top 10, CSA AICM/STAR),
and is multi-tenant, ACID, governable, and air-gappable. Prior
work treats the three layers separately: temporal-knowledge-graph memory systems
(Zep/Graphiti, Mem0g) unify **AI + DB** but carry no agent identity, governance, or
trust scoring; identity/access systems (Okta, SCIM, OpenFGA) provide the **agent**
layer but no AI memory/RAG; multi-model and graph databases (SurrealDB, ArangoDB,
Neo4j) provide the **DB** layer but not the AI+agent composite; benchmark layers
(SWE-bench, Agent-Bench) evaluate agents without providing the core itself. The
claim is deliberately falsifiable: not that any one capability is new, but that
their **composition into one resolvable, governable, trust-scored Agent OS core**
has not, to our knowledge, been published. We invite counterexamples.

## 2. Model

A **box** is `(id, kind, context, payload, provenance, state, realm)`. A **kind**
is a box (class); a **context** is a box (group/scope); a **relation** is a box;
edges connect boxes. Meaning is *defined and derived in context*; value, like
meaning, is contextual. **Validity:** *node→real* (every reference resolves) and
*box→stable* (every box filled, placed, typed); the graph must resolve at both.
The metamodel is in the graph, bottoming out at `kind:kind` (self-typed fixpoint),
so validating the graph validates the model. Full normative spec:
`fabric-of-work.md` (§0–§12), `fabric-substrate.md` (§6).

## 3. Methods (reference implementation)

All artifacts are deterministic (fixed seeds) and runnable without network:

| Artifact | Purpose |
|---|---|
| `scripts/fabric_graph.py` | resolves the constitution document itself (node+box) |
| `scripts/fabric_model.py` | self-describing stable-state model; JSON-LD; promotion; live streaming |
| `scripts/fabric_scale_bench.py` | synthetic graph, resolution throughput, 8e9 extrapolation |
| `scripts/fabric_rag_bench.py` | RAG / AI-memory / trust retrieval (speed, precision) |
| `scripts/fabric_agent_score.py` | Trust/Reliability/Usability/GPA + risk/threat |
| `experiments/fabric/*.surql` | SurrealDB backend schema, seed, resolve, live |

## 4. Results

**Resolution scale.** Linear; ~23.5M elements/s/core at 0.1–3M boxes (node-real,
box-stable held). 8×10⁹ boxes ≈ 584 GB raw → infeasible as one process, feasible
as ~160 federated shards of 50M (~3.6 GB, ~10–12 s each, parallel). Federation is
required by the model (§3.4), not bolted on.

**Retrieval (RAG / memory / trust).** Exact brute-force over 8,000 boxes (dim 16):
global RAG 88 q/s at precision@5 = 100%; **context-scoped memory 322 q/s (~3.7×)
at 100%**; trust-filtered retrieval 100% trusted. Context narrows the search,
improving speed at equal accuracy — the model's structural advantage. ANN indexing
would trade accuracy for 10–100× speed.

**Agent scoring.** Trust/Reliability/Usability composited into a 0–4 GPA (trust
weighted highest) with a risk/threat profile. Example: a mature agent scores
3.89 (A, Low risk); a drifting agent 2.21 (C+, Elevated) with explicit threats
(memory poisoning, unpinned provenance, instability). Trust is the binding
constraint, making the metric drift-resistant.

## 5. Substrate evaluation

We compare SurrealDB, SpacetimeDB, and PostgreSQL across graph-nativeness,
multi-model (doc/graph/vector), real-time (live + replay), ACID, edge/serverless,
pluggable storage, and the backend≠runtime separation the model requires
(`fabric-substrate-comparison.md`). SpacetimeDB fuses backend and runtime
(best real-time latency) but is relational and single-engine, conflicting with the
stateless control plane; PostgreSQL is a mature backend-only baseline; **SurrealDB
matches the box/graph model and the "backend, not runtime" decision most closely.**
*Caveat:* engines were not benchmarked head-to-head here (unavailable in the
environment); claims about SurrealDB/SpacetimeDB/Postgres are from their
documentation, cited below.

## 6. Use-case validation

Context store, feature store, AI registry, agent marketplace, agent lifecycle /
maturity, and cross-framework benchmarking each reduce to boxes-in-context that
resolve at node+box; only the filter, kind, and score differ
(`fabric-use-cases.md`).

## 7. Related work

W3C Decentralized Identifiers and Verifiable Credentials (identity as proof);
JSON-LD (`@context`, shared meaning); property-graph and multi-model databases
(SurrealDB); in-database compute (SpacetimeDB reducers); RDBMS (PostgreSQL);
agent task benchmarks (SWE-bench; HF Coding Agent Leaderboard); agent frameworks
and harnesses (Anthropic **Claude Agent SDK** and **Claude Code**, **LangGraph /
DeepAgents**, Nous Research **Hermes**, Alias Robotics **CAI** for security, and
others). LangGraph models an agent as a **state graph** of nodes and edges, which
maps directly onto the box graph — a LangGraph node is a box, its transitions are
relations — so such agents are hosted and scored natively. The fabric is **harness-
and model-agnostic**: any of these (open-weights like Hermes or hosted like Claude)
emits boxes-in-context and is scored on the same Trust/Reliability/Usability/GPA
and risk axes; open-weights models additionally enable the **air-gapped, local-LLM**
profile. The fabric's novelty is the **uniform, self-describing, resolvable**
treatment that unifies governance, retrieval, and trust scoring on one model.

## 8. Limitations and reproducibility

Benchmarks are **synthetic and single-machine**; cross-engine database benchmarks
were not run; 8e9 figures are **modeled extrapolations**; retrieval uses exact
search (no ANN); agent-scoring inputs are illustrative. All scripts are
deterministic and runnable (`python3 scripts/*.py`); the SurrealDB backend is
provided as SurrealQL + a testcontainer-style runner that falls back to the
in-process reference. We invite replication and adversarial re-derivation (§3.5).

## 9. Conclusion

A single self-describing graph model — boxes-in-context that must resolve at node
and box — suffices to govern, scale, retrieve, and trust agentic work, and to
serve many product use cases without new machinery. *One stable-state model, many
stores.*

## References

- W3C DID Core; W3C Verifiable Credentials Data Model.
- JSON-LD 1.1, W3C.
- SurrealDB — <https://surrealdb.com/>, features, 3.0 benchmarks.
- SpacetimeDB — key architecture, reducers, FAQ — <https://spacetimedb.com/docs/>.
- PostgreSQL documentation; pgvector.
- SWE-bench; HF Coding Agent Leaderboard — <https://hf.co/spaces/taagarwa/coding-agent-leaderboard>.
- Anthropic Claude Agent SDK.
