# Fabric — SWOT and Cost/FinOps Analysis

> Derived, contestable (`fabric-of-work.md` §12). Strategic assessment plus a
> cost-attribution model (OpenCost-aligned).

## SWOT

### Strengths
- **One minimal, self-describing model** (`box · kind · relation · context`) that
  **resolves at node + box** — validity is computed, not claimed.
- **Federated and infinitely scalable** (8B as ~160 shards), **minimal attack
  surface**, **air-gappable**.
- **Trust, provenance, resolution built in** → drift-resistant, governable,
  auditable; trust is the binding constraint (Agent GPA).
- **Multi-model / multi-use-case** — one substrate (SurrealDB) serves context
  store, feature store, AI registry, marketplace, ILM.
- **Reproducible, cited research**; **bleeding-edge** (bi-temporal); **framework-
  agnostic** scoring (LangGraph, Claude Agent SDK, …).

### Weaknesses
- **Early / conceptual**: no production deployment; benchmarks are synthetic and
  single-machine; **no head-to-head DB benchmark** run; 8e9 is modeled.
- **Governance under-specified operationally** — ratify/veto thresholds and the
  **IoA protocol are not implemented**.
- **Adoption cost**: buying into a new "everything is a box" ontology.
- **Tests** don't yet cover the new artifacts; repo CI is red (pre-existing
  `pytest-asyncio`).

### Opportunities
- **Surging demand** for agent memory/trust/governance (2025–26 research wave).
- **Standards alignment** (W3C DID/VC, JSON-LD, OWASP LLM Top 10, CSA AICM/STAR)
  → credibility and procurement fit.
- **Cost-aware agentic work** (FinOps) is largely unaddressed — see below.
- **Productization** of many stores from one substrate; **publishable** research;
  open-source community.

### Threats
- **Incumbents** with traction (Zep/Graphiti, Mem0, MemoriesDB).
- **Substrate lock-in** if coupled too tightly to one engine (mitigated: model is
  engine-neutral; SurrealDB is one backend).
- **Evolving attacks** — memory poisoning (MemoryGraft), supply-chain (mitigated,
  not solved).
- **Standards churn** and agent-framework fragmentation.
- **Over-abstraction skepticism** ("everything is a box").

## Cost / FinOps analysis (OpenCost-aligned)

Cost is a **data point** (value-in-context, §10.2), so the fabric can attribute it
on the same graph it already resolves.

- **Cost per construction** = Σ(labour compute + tool/API calls + ingredients),
  attributed via `performs` / `contains` / `commands` edges — a graph rollup, not
  a separate accounting system.
- **Cost per agent / context / tenant** = subtree sum over containment edges;
  multi-tenant isolation (§9.1) gives clean per-tenant allocation.
- **Value per cost** = an agent's produced `value` (§10.2) ÷ its cost → a
  **cost-efficiency** term that can extend the **Agent GPA**.
- **Real-time cost** via change feeds (§6.1): cost streams as work runs; budgets
  become **constraints** (§7, LLM10 unbounded-consumption defense).
- **Layering with OpenCost** — [OpenCost](https://github.com/opencost/opencost)
  (CNCF) measures the **infrastructure** cost of the runtime substrate
  (Kubernetes/cloud, §9.3); the fabric adds **work-level attribution** above it:
  OpenCost says *what the cluster cost*, the fabric says *which boxes,
  constructions, and agents incurred it*.

> Cost becomes just another resolvable, provenance-bearing dimension of a box —
> measurable and governable (§6) like everything else. *Maximize value per cost at
> every touch point* (§10.5).

## Resilience / chaos (chaos score)

Chaos-Mesh-style fault injection at the graph level (`scripts/fabric_chaos.py`)
measures a **chaos score** = fraction of the graph that still resolves after a
fault:

| Fault | Chaos score |
|---|---|
| random kill 1% | 96.1% |
| random kill 5% | 81.2% |
| random kill 10% | 65.8% |
| random kill 25% | 31.9% |
| **kill a whole shard** | **92–98% of surviving boxes intact** |

**Finding:** federation (§3.4) is a *resilience* mechanism, not only a scale one.
Unprotected random failure degrades the whole graph super-linearly (refs break);
a **shard kill is contained** — only cross-shard references *into* the dead shard
break, so every other shard stays intact. Pair with [Chaos Mesh](https://github.com/chaos-mesh/chaos-mesh)
for infra-level fault injection under the runtime substrate (§9.3); the fabric
adds the graph-level chaos score above it. Failures are explicit (§7.5).

## Bottom line

A differentiated, standards-aligned, drift-resistant substrate with strong
research footing; the work to de-risk is **production hardening, a real federated
protocol, and head-to-head benchmarks**. The cost angle is an open, winnable
opportunity.
