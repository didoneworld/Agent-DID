# Substrate Comparison — SurrealDB vs SpacetimeDB vs Postgres

> **Status:** Design evaluation — a **provider benchmark**. Derived, contestable
> (`fabric-of-work.md` §12). This is *not* a search for a vendor to depend on: the
> **contract is ours** (`fabric-substrate.md` §1.1), and each engine is scored by
> *how well it conforms to that contract*. Candidate backends are evaluated against
> the workloads that matter for an **agentic** system: RAG, AI memory, and trust —
> on **speed, accuracy, and real-time reaction** — plus the operating-mode axes
> (edge, serverless, hybrid cloud, streaming, ACID, multi-model). The winner
> *hosts* the contract best; none *owns* it.

## The agent workloads are one shape

In the fabric, RAG, AI memory, and trust are the **same shape** — a box is
data-in-context (§10):

- **RAG** — retrieve boxes by similarity (vector over payload).
- **AI memory** — retrieve durable boxes scoped to a **context** (memory-in-context).
- **Trust** — retrieve only **ratified, provenance-bearing** boxes (§3.1, §3.3).

One model serves all three; the substrate must provide **vector + graph +
real-time** over the same records.

## The most important number for us

For an agent, the decisive metric is **trusted recall at real-time latency** —
*did the agent retrieve the right, trusted context, fast enough to react?*
Everything else is secondary. This is also the antidote to **AI drift**: if
retrieval is restricted to **resolved (real + stable), provenance-bearing,
ratified** boxes, the agent cannot silently drift onto stale or unfounded
memory — meaning stays derived and re-derivable (§2, §3.5).

Measured (`scripts/fabric_rag_bench.py`, exact brute-force, pre-ANN):

| Scenario | Throughput | Accuracy | Trusted |
|---|---|---|---|
| RAG (global vector search) | 88 q/s (11.3 ms) | precision@5 = **100%** | 81% |
| **AI memory (context-scoped)** | **322 q/s (3.1 ms)** | **100%** | 77% |
| Trust (ratified-only) | 106 q/s (9.4 ms) | 100% | **100%** |

**Key result:** context-scoping is **~3.7× faster at equal accuracy** — because
*data-in-context narrows the search* (§10.4). The trust filter delivers **100%
trusted** retrieval. So the fabric's box/context model directly maximizes the
metric that matters: *trusted recall, in real time.* (An ANN index trades a little
accuracy for 10–100× more speed.)

Graph-resolution throughput (`scripts/fabric_scale_bench.py`): **~23.5M
elems/s/core, linear**; 8B boxes → 160 federated shards (§3.4).

## Capability matrix

Legend: ✅ strong · ◐ partial / via extension · ✗ weak

| Axis (fabric need) | **SurrealDB** | **SpacetimeDB** | **Postgres** |
|---|---|---|---|
| Graph-native (boxes/edges §9) | ✅ SurrealQL traversals | ◐ relational | ◐ recursive CTE / AGE ext |
| Multi-model (doc+graph+vector) | ✅ | ✗ relational | ◐ extensions |
| RAG / vector search | ✅ native vectors | ✗ | ◐ pgvector |
| AI memory (data-in-context) | ✅ records + ctx + vectors | ◐ tables | ◐ tables + pgvector |
| Trust / provenance (graph §3.1) | ✅ graph edges + RLS | ◐ in-module logic | ◐ FKs + app logic |
| Speed — hot path | ✅ in-mem / edge | ✅✅ in-memory reducers (lowest latency) | ◐ disk-based, mature |
| ACID transactions | ✅ | ✅ reducer = transaction | ✅✅ gold standard |
| Real-time **live stream** | ✅ LIVE SELECT | ✅✅ direct subscriptions | ◐ LISTEN/NOTIFY |
| **Re-stream** / replay | ✅ CHANGEFEED | ◐ commit log | ◐ logical replication / WAL |
| Edge / embedded / WASM | ✅✅ browser, device | ✗ server | ✗ server |
| Serverless | ✅ | ◐ hosted | ◐ (e.g. Neon) |
| Hybrid cloud / pluggable storage | ✅✅ mem · SurrealKV · RocksDB · TiKV · FDB | ◐ single engine | ◐ single engine |
| Backend ≠ runtime (stateless CP) | ✅ backend; runtime above | ✗ **fuses** runtime into DB | ✅ backend |
| Multi-tenant / federation (§3.4) | ✅ namespace / database | ◐ per-module | ◐ schema / database |

## Reading the three

- **SpacetimeDB** *fuses backend and runtime*: app logic runs inside the DB as
  transactional **reducers**, clients subscribe directly to live tables, all state
  in memory + commit log. **Best-in-class for real-time reaction and low-latency
  speed.** But it is relational (weak on graph/vector → RAG, memory, trust need
  bolting on), single-engine (weak on edge/serverless/pluggable storage), and it
  *contradicts the constitution's separation of runtime from backend* (§9.3) and
  the stateless control plane (`design-principles.md` §2).
- **Postgres** — the gold standard for ACID and ecosystem maturity, but a
  **backend only**: graph and vector are extensions, real-time is bolt-on, and it
  needs a separate runtime tier. A conservative, proven fallback.
- **SurrealDB** — multi-model (doc + graph + vector) with **LIVE SELECT +
  CHANGEFEED** (live *and* re-stream), ACID, runs **embedded / edge / serverless /
  distributed** with **pluggable storage**, and isolates tenants by
  namespace/database. It matches the fabric's box/graph model and the "backend,
  not runtime" decision almost 1:1.

## Recommendation

1. **SurrealDB is the backend (BE + DB).** It alone covers, natively, every axis
   the agent workloads need: graph (trust), vectors (RAG, memory), live + replay
   streaming, edge/serverless/hybrid with pluggable storage, ACID, and
   federation — while keeping the runtime *above* it (§9.3, stateless control
   plane). This is the existing decision, now justified against alternatives.
2. **Borrow SpacetimeDB's patterns for the real-time runtime layer** — in-memory
   hot state, direct client subscribe, deterministic transactional reducers — for
   latency-critical *constructions*, without fusing logic into the system of
   record.
3. **Keep Postgres (+ pgvector) as a conservative fallback backend** where
   ecosystem maturity outweighs graph-native modeling.

> The most important number is **trusted recall at real-time latency**. The
> box/context model maximizes it (context-scoping: 3.7× speed at 100% accuracy;
> trust filter: 100% trusted), and SurrealDB is the backend that serves it across
> all operating modes.

## Deployment profile: air-gapped, local LLM, edge

The agent workloads (RAG, memory, trust) plus the backend can run **fully local /
air-gapped**, which is the strongest posture for both **trust** and **minimal
attack surface** (§5.2):

- **Embedded backend** — SurrealDB runs in-process / on-device / in the browser
  (WASM), so the system of record needs **no server and no network**. SpacetimeDB
  (server) and Postgres (server) are weaker here.
- **Local LLM** — reasoning, embeddings, RAG, and memory stay **on-device**: no
  external dependency, no data exfiltration, and no drift from outside sources —
  the agent reasons only over its **trusted, resolved** memory.
- **Air-gapped** — with **zero external ingress**, there is almost nothing to
  attack and data never leaves the boundary. The most secure agent is a sealed
  one: embedded SurrealDB + local LLM + the box/context model.
- **Ingress** is the one governed seam. Where it exists it is **context-enforced
  (§1.4) and least-privilege**; air-gapped = no ingress = strongest posture.
  Edge/serverless modes (§9.3) make the same stack deployable from a laptop to a
  sealed facility — *the structure stays constant; only the substrate changes.*

This is the **agent-clear** profile: a self-contained agent whose memory is
local, trusted, real-time, and resolvable — drift-resistant by construction.

## Additional substrates: SingleStore, ClickHouse, OceanBase

Three distributed SQL engines worth weighing. **None is graph-native or
edge-embeddable** (all are server/cluster), so none fits the box-graph + air-gapped
core as well as SurrealDB — but each is a strong **complement** for one layer
(polyglot persistence, §6.8).

| Axis | **SingleStore** | **ClickHouse** | **OceanBase** |
|---|---|---|---|
| Model | distributed HTAP SQL (row+column) | columnar OLAP | distributed HTAP SQL (MySQL/Oracle-compat) |
| Graph-native (boxes/edges) | ◐ relational | ✗ | ◐ relational |
| Vector / RAG | ✅ ANN (≈800–1000× vs KNN) | ◐ approximate vector | ◐ emerging vector |
| Real-time | ✅ HTAP, lock-free ingest (M events/s) | ✅ very fast inserts/reads (append) | ✅ HTAP |
| ACID / transactions | ✅ | ◐ limited | ✅✅ distributed (Paxos), extreme scale |
| Analytics / cost rollups | ✅ TPC-H/DS-class | ✅✅ best-in-class OLAP | ✅ |
| Edge / embedded / air-gap | ✗ server / cloud | ✗ server | ✗ server |
| Backend ≠ runtime | ✅ backend | ✅ backend | ✅ backend |

- **SingleStore** — best **HTAP + native vector** at cloud scale; excellent for the
  **RAG/memory + real-time analytics** layer where graph traversal isn't the hot
  path. ([SingleStore-V](https://www.singlestore.com/resources/research-paper-singlestore-v-an-integrated-vector-database-system-in-singlestore/),
  [agentic AI architecture](https://www.singlestore.com/blog/real-time-data-convergence-architecture-agentic-ai-hitech/))
- **ClickHouse** — best-in-class **OLAP**; ideal for the fabric's **measurability/
  cost/audit** layer — change-feed archives, telemetry, cost rollups (§6.3, FinOps)
  — not the transactional box store.
- **OceanBase** — **distributed ACID at extreme scale** (Paxos, HA); a durable
  transactional backbone for very large federations where SQL maturity and
  cross-shard transactions dominate.

**Net:** keep **SurrealDB as the primary box-graph backend** (graph + multi-model +
edge/air-gap). Complement with **SingleStore/ClickHouse** for vector-and-analytics
at scale and **OceanBase** for massive ACID — a polyglot-persistence story that
leaves the box model unchanged (§6.4): only the engine behind a context/shard
differs.

## Graph-native and compute engines: Neo4j, ArangoDB, Spark, Convex

These sit closest to the box-graph core — two are graph-native (direct SurrealDB
alternatives), one is a compute engine, one fuses runtime.

| Axis | **Neo4j** | **ArangoDB** | **Apache Spark** | **Convex** |
|---|---|---|---|---|
| Model | native graph | multi-model (doc+graph+kv) | distributed **compute** (not a store) | reactive backend (doc) |
| Graph-native | ✅✅ Cypher + GDS algorithms | ✅ AQL traversals | ◐ GraphX / GraphFrames | ✗ |
| Multi-model / vector | ◐ + vector index | ✅ + vector | n/a (processes any) | ◐ |
| Real-time | ◐ change data capture | ◐ | ✅ Structured Streaming (batch+stream) | ✅✅ reactive subscriptions |
| ACID | ✅ | ✅ | n/a | ✅ |
| Edge / embedded / air-gap | ◐ embedded (JVM) | ◐ | ✗ cluster | ✗ hosted |
| Backend ≠ runtime | ✅ backend | ✅ backend | ✅ compute/runtime layer | ✗ **fuses** runtime (TS funcs) |

- **Neo4j** — best-in-class **graph algorithms** (GDS) and Cypher; ideal for the
  **trust/provenance/lineage** graph and `derives`-edge reasoning. A credible swap
  for the box-graph backend; chosen against only because it is graph-mostly
  (weaker multi-model/vector) and server-centric.
- **ArangoDB** — the closest **multi-model + native graph** alternative to
  SurrealDB; either could host the box graph. SurrealDB is preferred for
  edge/WASM, live queries, and pluggable storage, but ArangoDB is a near-peer.
- **Apache Spark** — not a store but the **distributed compute/runtime** layer:
  offline resolution of huge graphs (GraphFrames), federation ETL, training, and
  batch analytics over the box graph at 8e9 scale (§9.3). Complements the backend,
  it doesn't replace it.
- **Convex** — a **reactive backend** (TypeScript functions + reactive DB) that,
  like SpacetimeDB, **fuses backend and runtime**: great real-time/serverless DX,
  but weak graph/vector, hosted (no air-gap), and conflicts with the stateless
  control plane / backend≠runtime decision (§9.3).

**Net (all substrates):** the box model is **engine-neutral** (§6.4). SurrealDB is
the primary backend (graph + multi-model + edge/air-gap); Neo4j/ArangoDB are
credible graph-native swaps; SingleStore/ClickHouse/OceanBase serve the
vector-analytics/ACID-at-scale layers; Spark is the offline compute engine;
SpacetimeDB/Convex are deliberate non-fits (they fuse runtime). *One model, many
engines — chosen per context/shard.*

## Security risk vs blockchain / The Graph

A different trust model is worth contrasting: **blockchain** (global consensus +
immutability) and **The Graph** (decentralized indexing of on-chain data via
subgraphs). The fabric uses **federated provenance + ratification + resolution**
instead of a global ledger.

| Security axis | **Fabric** | **Blockchain** | **The Graph** |
|---|---|---|---|
| Trust model | federated provenance + ratify + resolve (§3) | global consensus / immutability | decentralized indexers + staking/curation |
| Attack surface | minimal: one box type, context-enforced, air-gappable | smart-contract bugs, 51%/MEV, bridge hacks | indexer/curation economics + underlying chain |
| Privacy | context-enforced; air-gapped possible (§9) | **public by default** (bad for private agent work) | public (indexes public chains) |
| Latency / cost | real-time, cheap | slow finality, gas cost | query latency + chain finality |
| Tamper-evidence | provenance + change feeds (tamper-evident) | **strong** (global immutable ledger) | inherits chain |
| Governance | **reasoned, contestable, re-derivable** (§3.5) | code-is-law; hard to amend | token governance |
| Data residency | local / edge / sovereign | global replication | global |

**Assessment.** Blockchain buys *global trustlessness and immutability* at the cost
of **public exposure, latency, gas, and a large smart-contract attack surface** —
the wrong trade for private, real-time, governed agent work. The Graph's subgraph
model is conceptually close (graph queries) but anchored to public chains. The
fabric instead minimizes attack surface (air-gappable, one type, context-enforced)
and makes trust **computable and contestable** rather than globally immutable —
**lower security risk for private agentic work**, at the cost of not being
globally trustless. Where global immutability is genuinely required, a fabric box
can *anchor* a provenance hash on-chain without moving the data — trust without
exposure.

---

**Sources:** [SpacetimeDB key architecture](https://spacetimedb.com/docs/intro/key-architecture/),
[SpacetimeDB reducers](https://spacetimedb.com/docs/functions/reducers/),
[SpacetimeDB FAQ](https://spacetimedb.com/docs/intro/faq/),
[SurrealDB](https://surrealdb.com/), [SurrealDB features](https://surrealdb.com/features),
[SurrealDB 3.0 benchmarks](https://surrealdb.com/blog/surrealdb-3-0-benchmarks-a-new-foundation-for-performance).
