# The Fabric Substrate — Data Model, Store, and Experimentation Environment

> **Status:** Design proposal. **Derived, not decreed** (cf.
> [`fabric-of-work.md`](./fabric-of-work.md) §12): this is a ratified-pending
> derivation, open to re-derivation and contest. It makes the constitution's
> abstractions (**data-in-context**, **boxes**, **graph**, **schema**, **operating
> modes**) concrete on a real substrate.

This document answers four questions raised against the constitution:

1. Can **SurrealDB** serve as the substrate?
2. What is the **ideal data model**?
3. What is the **ideal structure for maximum efficiency**?
4. What is the **experimentation environment**?

---

## 1. Why SurrealDB Fits the Fabric

The constitution demands a substrate that is graph-shaped, data-first, and able
to be *schemaless but never structureless*. SurrealDB maps onto the constitution
almost one-to-one:

| Constitution requirement | SurrealDB capability |
|---|---|
| **Graph / DAG mode** (§9.1) — work is a graph of boxes and edges | native graph: records + `RELATE` edges, multi-hop traversal |
| **Schemaless ok, structureless no** (§7.6.4) | `SCHEMALESS` tables for payloads **and** `SCHEMAFULL` tables for envelopes/relations — structure always present |
| **Data is primary** (§10) | record-first, document + relational + graph in one model; data carries its own links |
| **Context is enforced** (§1.4) | record links, table permissions, and field assertions enforce context at write/read |
| **Multi-tenant** (§9.1) | `namespace` / `database` isolation per tenant |
| **Experimentation env** (§8.4.2) | ephemeral `namespace`/`database` as a sandbox (a virtual box) |
| **Continuous** (§6.1) | live queries / change feeds for reactive work |
| **Governable, measurable** (§6.3–§6.4) | embedded provenance/value fields queried without joins |
| **Multi-environment / edge / cloud** (§9.3) | embedded (in-memory / file) **and** distributed server modes |

The decisive fit is **SCHEMAFULL + SCHEMALESS coexisting**: the fabric can be
schemaless where flexibility is needed and schemafull where structure must be
guaranteed — *schemaless but never structureless*, exactly §7.6.4.

### 1.1. The contract is ours — SurrealDB is a *feature*, not a *provider*

The architectural stance, stated plainly:

- **The contract is ours.** The box model, the `@context`, the **resolution
  invariant** (node + box → real + stable), the operating semantics, and the
  trust/provenance rules are owned by the fabric. A substrate does **not** define
  the contract — it **conforms** to it. This is dependency inversion: we depend on
  our abstraction (`box` / `resolve`), never on a vendor's API.
- **The vendor is a feature, not a provider.** SurrealDB is an open-source single
  binary embedded **inside our boundary** (in-process, WASM, edge, air-gapped) —
  a capability we compose, like a library; we own the data, uptime, and lifecycle.
  A *provider* (hosted, owning, sticky — e.g. SpacetimeDB, Convex) would invert
  that and own us. We use the store strictly as a feature.
- **Therefore vendor-neutrality is structural, not aspirational.** Any engine that
  satisfies the contract is interchangeable (Neo4j, ArangoDB, Postgres, SingleStore
  …). The contract is the moat; the engine is swappable.
- **The substrate comparison is a *provider benchmark*.** Engines are scored by
  *how well they conform to our contract* (graph, schemaless-not-structureless,
  live + replay, edge/embed, ACID, backend≠runtime) — not by which one we are
  locked into. The winner **hosts** the contract best; none **owns** it. (See
  `fabric-substrate-comparison.md`.)

> Provider logic makes the vendor hold the contract and you conform. The fabric
> holds the contract and the vendor conforms. For an identity/trust control plane,
> *who holds the contract* is the whole game.

---

## 2. The Ideal Data Model

### 2.1. One universal node: the **box**

Everything is a **box** (a node, §7.7) — uniform so traversal and composition are
uniform (§5.3). A box is *data-in-context with provenance and state.*

`box` table — **SCHEMAFULL envelope, SCHEMALESS payload**:

| Field | Meaning | Constitution |
|---|---|---|
| `id` | stable identity (a data point) | §10.2 |
| `kind` | `command \| tool \| ingredient \| labour \| construction \| strategy \| planning \| agent \| schema \| context` | §8 |
| `context` | record link → `context` (the slot it is placed in) | §1, §7.7 |
| `realm` | `real \| digital` | §8.4 |
| `state` | `proposed \| ratified \| stable \| revoked` | §3.3, resolver |
| `value` | asset value as a data point (number/object) | §10.2 |
| `provenance` | `{ derived_by, from[], evidence[], at }` | §3.1 |
| `schema_ref` | optional link → a `kind:schema` box | §7.6 |
| `payload` | schemaless data — the box's contents | §7.6.4 |

### 2.2. Context is a first-class record

`context` table (**SCHEMAFULL**): `{ id, name, parent → context, schema, policy }`.
Meaning and value are derived *in* a context (§1, §10.4); making context a record
means the *same datum* can be linked into different contexts and resolve to
different value — useless in one, invaluable in another (§10.4).

### 2.3. Edges (graph relations via `RELATE`)

| Edge | From → To | Meaning |
|---|---|---|
| `contains` | box → box | containment / slot filling (§7.7) |
| `references` | box → box | cross-reference (node resolution) |
| `derives` | box → box | derivation lineage (§2, §3.1) |
| `derived_by` | box → agent | who reasoned it (§3.1) |
| `fills` | box → context | a box placed into a context-slot (§7.7) |
| `commands` | agent → box | a command (§8.2) |
| `performs` | agent → construction | labour (§8.2) |

### 2.4. Identity and value are data points

An **agent** is a box of `kind:agent` (DID-anchored) — *identity is a data point*
(§10.2), bridging to the existing Agent ID record. **Asset value** is the `value`
field — *value is a data point* (§10.2), and because it links to `context`, it is
always **value-in-context** (§10.4).

### 2.45. Schemaless payload, multimedia, and concurrency

- **Schemaless payload, multimedia file types.** The `payload` is schemaless
  (§7.6.4), so a box holds **any** content: text, JSON, or **multimedia** — images,
  audio, video, PDFs — stored as blob references plus **vector embeddings** for
  RAG/memory (§4). The envelope stays schemafull (never structureless); the
  contents are free. One box type carries every modality.
- **Concurrency.** Many constructions proceed at once (multi-threaded mode,
  §9.1). Writes are **ACID**; box updates use optimistic concurrency; and because
  resolution is per-shard and per-context, **resolution parallelizes** without
  global locks (stateless control plane, `design-principles.md` §2).

### 2.5. Validity = the resolver, in the store

A box is **valid (real + stable)** under the same criteria as
`scripts/fabric_graph.py`:

- **node → real:** every `references` / `contains` / `derives` edge resolves to an
  existing box (no dangling). Enforceable as a SurrealDB query over edges.
- **box → stable:** `filled` (payload or contained boxes), `placed` (has
  `context` + parent), and `schema_ref`-valid.

The same resolver can run as a stored validation: *the constitution checks itself
inside its own substrate.*

---

## 3. Ideal Structure for Maximum Efficiency

1. **One node type, typed by `kind`** — uniform traversal; no per-type join graph
   (composability §5.3).
2. **Graph-native links** — resolution is edge traversal (`->references->`), not
   relational joins; node/box resolution is cheap and local.
3. **Embedded provenance and value** — governance and measurement (§6.3–§6.4)
   read from the record, no join fan-out.
4. **Context as a link, not a copy** — store a datum once, link it into many
   contexts; value-in-context (§10.4) without duplication. *Maximize value at
   every touch point* (§10.5) becomes "link the datum into the highest-value
   context," an O(1) edge.
5. **SCHEMAFULL envelope / SCHEMALESS payload** — validate what must be stable,
   stay flexible elsewhere (§7.6.4).
6. **Live queries / change feeds** — continuous, reactive work (§6.1); no polling.
7. **Indexes on `(context, kind, state)`** — the hot path: "stable boxes of a kind
   in a context."
8. **Namespace/database per tenant** — isolation (§9.1) with no cross-tenant cost.

Efficiency principle: **store data once, contextualize by linking, resolve by
traversing.** Value is maximized by *placement* (which context a datum is linked
into), not by *copying* — and stability is maintained by keeping every edge
resolving (§10.6).

---

## 4. The Experimentation Environment

The experimentation environment is the constitution's **virtual box / sandbox**
(§8.4.2) made concrete: an **ephemeral SurrealDB `namespace`/`database`** that is
fully isolated and digital-only (§8.4) — nothing in it touches the real world.

### 4.1. Lifecycle

1. **Spawn** — create an ephemeral namespace; load the fabric schema
   (`SCHEMAFULL` envelopes, edges) and snapshot the relevant `context` boxes.
2. **Import** — concepts are imported as `realm:digital` boxes in `state:proposed`
   (§8.4.2). No real-world effect.
3. **Construct** — agents derive meaning, fill slots, build constructions; every
   step carries provenance (§3.1).
4. **Resolve** — run the resolver (§2.5) over the sandbox: must be **node-real**
   and **box-stable** (the `fabric_graph` criteria).
5. **Ratify** — federated procedure (§3.3): evaluate, vote, reasoned veto.
6. **Promote** — only boxes that *resolve* and are *ratified* are promoted to the
   real environment and may become `realm:real`. Everything else is discarded
   with the sandbox.

### 4.2. Guarantees

- **Safe** — digital-only until promoted; the seam between digital and real is
  governed (§8.4.3) and context is enforced at the boundary (§1.4).
- **Observable** — measurable (§6.3); every derivation and value is recorded.
- **Reproducible** — a sandbox is a snapshot + a derivation log; re-derivable by
  anyone (§2.2, the right to reason §3.5).
- **Disposable** — the namespace is the unit of cleanup; failed experiments leave
  no residue (stateless control plane, §9.1).

> The experimentation environment is where **digital work** (§8.4) happens at full
> speed under full governance, and only **real, stable, ratified** work crosses
> into the real world. *Maximize value, stabilize state — first in the sandbox,
> then for real.*

---

## 5. Scale and Attack Surface

### 5.1. Can it resolve at 8 billion nodes? (one box per person)

Measured with `scripts/fabric_scale_bench.py` (synthetic, fully resolvable graph,
avg degree 4, single core):

| Boxes | Edges | Resolve | node | box | Rate |
|---|---|---|---|---|---|
| 100,000 | ~400,000 | 0.03 s | real | stable | ~17 M elems/s |
| 1,000,000 | ~4,000,000 | 0.21 s | real | stable | ~24 M elems/s |

Resolution is **linear** (~20 M elements/s/core), and stays **node-real +
box-stable** at every size. Extrapolated to **8×10⁹ boxes**:

- Raw data footprint (model, ~73 B/box): **≈ 584 GB** — too large for one process.
- **Verdict: not feasible as one monolithic graph; feasible as a federation.**

This is not a workaround — it is the constitution. **§3.4 (federated, not
captured)** and **§3.7 (Internet of Agents)** *require* federation. 8 billion
boxes is one identity per person: the Internet of Agents, federated by
construction.

| Federated plan | Value |
|---|---|
| Shard size (per federation) | 50,000,000 boxes |
| Shards for 8×10⁹ | ~160 |
| Footprint per shard | ~3.6 GB (fits one engine) |
| Resolve per shard (1 core) | ~12 s → in parallel ≈ same wall-clock |

Each shard **resolves at node + box locally**; cross-shard references resolve via
the **IoA protocol** (§3.7). The resolver in `scripts/fabric_graph.py` is the
per-shard validator; planetary validity is the conjunction of resolved shards.

### 5.2. Minimal attack surface

The data model is chosen for a **small, uniform, governable** surface:

- **One node type (`box`)** → one small read/write API; nothing bespoke per kind
  to attack (§5.3 composability).
- **SCHEMAFULL envelopes** reject malformed input at the boundary; failure is
  explicit (§1.4, §7.5).
- **Context enforced per operation** — every read/write is scoped to a context /
  namespace; no ambient authority (§1.4).
- **Digital-only sandbox until promotion** (§8.4) — experiments cannot touch the
  real world; the digital→real seam is governed (§8.4.3).
- **Stateless control plane** (§9.1; `design-principles.md` §2) — no session state
  to steal or replay.
- **Least privilege** — command/capability boxes are scoped to a context
  (`design-principles.md` §14).
- **Federation bounds blast radius** — compromise of one shard/tenant does not
  cascade; there is **no central authority to capture** (§3.4). The same property
  that makes meaning uncapturable makes the system hard to own.
- **Provenance on every box** (§3.1) — tamper-evident and auditable (§6.3).

Security and the constitution coincide: *federated, context-enforced,
least-privileged, provenance-bearing* is both the governance model and the
minimal-attack-surface model.

---

## 6. The Model is the Graph — the Smallest, Stable-State Model

Implemented and validated in `scripts/fabric_model.py`.

6.1. **The model is not above the graph; it is in the graph.** The metamodel —
the kinds, the relations, even `schema` — are **boxes**, typed by boxes, related
by boxes. The type chain terminates in a **self-typed fixpoint**: *a `kind` is a
`kind`*. There is nothing privileged outside the graph; the graph describes
itself (cf. §7.6.3 "a schema is itself a box").

6.2. **A box is data and meaning.** Each box carries *data* (payload) and
*meaning* (its kind + context). Data-in-context (§10) **is** the box; the model is
just more boxes. There is no second substance.

6.3. **This is the smallest model.** One node type (box), one edge notion
(relation — itself a box), one fixpoint (`kind:kind`). Commands, tools, agents,
schemas, contexts, and the model itself are all expressed in this single kernel.
Nothing smaller can still **describe itself and resolve**.

6.4. **Infinitely scalable.** With exactly one uniform type and one uniform edge,
the graph shards without special cases (§5.1): every shard is the same kernel;
federation composes kernels with no new machinery. **The model is constant as the
data grows** — minimal model, unbounded graph.

6.5. **Minimal attack surface.** One box type and one edge type mean one tiny,
uniform API to defend (§5.2). There is no out-of-band schema engine to subvert,
because the schema is *in* the graph and resolves like everything else.

6.6. **Maximize value, stabilize state.** Value is maximized by *placement* — the
context a box is linked into (§10.5) — and state is stabilized by keeping every
box resolved (§10.6). The model is "found" when it reaches its **stable state**:
the fixpoint where the graph, *including its own model*, resolves at **node (real)
and box (stable)**.

6.7. **The model must resolve — and at the stable state, it does.** Validated
result: 26 boxes (13 kinds, 7 relations, 6 data), every box typed by a box, every
edge related by a box, `kind:kind` fixpoint true, **NODE real (0 dangling), BOX
stable (0 unstable, 0 unreachable) → VALID**.

> The smallest model that can describe itself, resolve at node and box, scale
> without limit, and present the smallest attack surface is: **one box, typed by a
> box, related by a box, bottoming out in a box that is its own type.** That is the
> stable state.

6.8. **Polyglot: one kernel, many paradigms.** The kernel has four primitives —
**box**, **kind**, **relation**, **context** — and each is just the familiar idea
from every modeling language under a different name. This is why the model is
**polyglot**: the same graph renders natively into OOP, property graphs, RDF,
relational, and document stores without translation loss.

| Kernel primitive | OOP | Property graph | RDF / triples | Relational | Document |
|---|---|---|---|---|---|
| **box** (node) | object / instance | node | subject / resource | row | document |
| **kind** | **class** | label | `rdfs:Class` | table | type |
| **relation** | association / reference | edge | predicate | foreign key | embedded link |
| **context** | **group** / scope | named graph | named graph | schema / tenant | collection |

Because the kernel *is* these ideas, the fabric speaks every dialect: a box is an
object to an app, a node to a graph engine, a triple to a reasoner, a row to SQL,
a document to a store — **one stable-state model, many tongues.**

---

## 7. Mapping Summary

```
constitution (fabric-of-work.md)        substrate (this doc / SurrealDB)
------------------------------------    ------------------------------------
box (§7.7)                          ->  box record (kind-typed)
context (§1, §10.4)                 ->  context record (linked)
graph / node resolution (§9, §2.5)  ->  RELATE edges + traversal
schema (§7.6)                       ->  SCHEMAFULL tables + kind:schema boxes
schemaless ok, structureless no     ->  SCHEMALESS payload / SCHEMAFULL envelope
data is primary (§10)               ->  record-first, links carry meaning
value in context (§10.4)            ->  value field + context link
maximize value @ touch point (§10.5)->  link datum into highest-value context
stabilize (§10.6)                   ->  resolver: node real + box stable
multi-tenant / sandbox (§9.1, §8.4.2)-> namespace/database isolation
edge..cloud (§9.3)                  ->  embedded + distributed modes
```

This substrate makes the constitution **executable**: the same graph that must
*resolve at node and box* to be valid (real) is the graph the database stores,
links, and checks.
