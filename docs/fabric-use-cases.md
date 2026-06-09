# Use-Case Validation — One Model, Many Stores

> Derived, contestable (`fabric-of-work.md` §12). Validates that the box/context
> model + SurrealDB backend serves real product use cases **without new
> machinery** — each is the same kernel (`box · kind · relation · context`)
> filtered and scored differently.

A use case is "valid" on the fabric iff it reduces to **boxes-in-context that
resolve at node + box** (real + stable), with the operating modes (§9) supplying
its non-functional needs. Below, each does.

## 1. Context store ✅

The native case. A `context` (group/scope, §1) holds boxes; meaning and value are
derived in context (§10.4). Retrieval is context-scoped (3.7× faster at equal
accuracy — `fabric_rag_bench.py`). The `@context` is JSON-LD on the wire (§3.7).
*Validation:* the fabric **is** a context store.

## 2. Feature store ✅

A feature is a `box` of `kind:feature` in a context, versioned (`derives` edges),
provenance-bearing (§3.1), with a `value`.

- **Online serving** → real-time `LIVE SELECT` (low-latency reads, §6.1).
- **Offline / training** → `CHANGEFEED` **re-stream** for point-in-time replay.
- **Consistency** → ACID writes; context enforcement prevents train/serve skew
  (§1.4). *Validation:* online + offline feature store with one model.

## 3. AI registry ✅

Models, datasets, prompts, and evals are boxes (`kind:model | dataset | prompt |
eval`). Lineage is `derives` edges; versions are boxes; governance is
`state ∈ {proposed, ratified, stable, revoked}` (§3.3) and `realm` (§8.4).

- Promotion gated on **resolve + ratify** (digital→real, §8.4.3) = a real model
  registry with governance and provenance baked in.
- *Validation:* a registry where every entry is **resolvable and provenanced** —
  no orphan artifacts (node-real), no half-defined records (box-stable).

## 4. Agent marketplace ✅

Agents are boxes (`kind:agent`, DID-anchored). Discovery = context/capability
query; ranking = the **Agent GPA / Trust / Risk** scorecard
(`docs/fabric-agent-scoring.md`).

- Trust-ranked, drift-resistant listings; risk & threat profile per agent.
- Federated discovery across shards via the IoA protocol (§3.7) — no central
  marketplace owner (§3.4).
- External analog: SWE-bench-style [Coding Agent Leaderboard](https://hf.co/spaces/taagarwa/coding-agent-leaderboard).
  The fabric adds **trust + risk + provenance** that a pure task-success
  leaderboard omits. *Validation:* a marketplace whose rankings are computed from
  resolvable, provenance-bearing data.

## 5. Agent lifecycle management & product maturity ✅

An agent's lifecycle is its `state` machine: `proposed → ratified → stable →
revoked` (§3.3), mirroring the repo's existing ILM states (active / suspended /
revoked; `design-principles.md` §9). Promotion between states is gated on
**resolve + ratify + GPA/risk thresholds**.

- **Maturity** = sustained Trust + Reliability with bounded Risk over time
  (`fabric_agent_score.py`); a maturing agent's GPA rises and risk falls.
- Revocation and quarantine are state transitions, audited by provenance.
- *Validation:* lifecycle and maturity are **measured, not asserted** — the same
  resolution + scoring that validate the graph validate the agent's stage.

## 6. Cross-framework agent benchmarking ✅

The Agent GPA / Trust / Risk scorecard (`fabric_agent_score.py`) is
**framework-agnostic**: it scores an agent from the **resolvable, provenance-
bearing boxes it produces** — its memory, constructions, and provenance — not from
its internals. So agents built on **any** framework can be benchmarked on the same
axes and ranked side by side:

- Anthropic **Claude Agent SDK** agents, OpenAI Assistants, LangChain/LangGraph,
  CrewAI, AutoGen, custom harnesses — all emit boxes-in-context; all are scored
  identically.
- Task-success harnesses (SWE-bench, [Coding Agent Leaderboard](https://hf.co/spaces/taagarwa/coding-agent-leaderboard))
  feed **Usability/Reliability**; the fabric adds **Trust + Risk + provenance**,
  which framework-internal benchmarks omit.

*Validation:* a neutral, cross-framework benchmark — because the unit of
measurement is the box graph every framework writes into, not the framework.

## Why one model suffices

| Use case | kinds used | mode/property it leans on |
|---|---|---|
| Context store | context, * | context enforcement (§1.4) |
| Feature store | feature | live + re-stream (§6.1), ACID |
| AI registry | model/dataset/prompt/eval | provenance + state + promotion (§3, §8.4) |
| Agent marketplace | agent | scoring + federation (§3.7) |
| Lifecycle / maturity | agent + state | resolve + ratify + GPA gates |

All five are **boxes-in-context that must resolve at node + box**. The model does
not change per use case (§6.4); only the filter, the kind, and the score change.
That is the validation: *one stable-state model, many stores.*
