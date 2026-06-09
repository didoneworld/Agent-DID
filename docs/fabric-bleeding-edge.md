# Bleeding-Edge Scan — Agent Memory, Temporal Graphs, and Where the Fabric Sits

> Derived, contestable. A 2025–2026 landscape scan positioning the Fabric of Work
> against current research, and the one upgrade adopted as a result.

## Landscape (2025–2026)

| Work | Idea | Relation to the fabric |
|---|---|---|
| Graphiti / Zep | **bi-temporal** knowledge graph: every fact has `valid_at`/`invalid_at` | **adopted** (see below) |
| RoMem ([2604.11544](https://hf.co/papers/2604.11544)) | continuous phase rotation for temporal KGs | temporal validity |
| Mem0g | directed labeled graph memory, strong temporal reasoning | box graph + temporal |
| MemoriesDB ([2511.06179](https://arxiv.org/abs/2511.06179)) | temporal-semantic-relational unified store | multi-model substrate (SurrealDB) |
| Memanto ([2604.22085](https://hf.co/papers/2604.22085)) | **typed** semantic memory, deterministic retrieval | typed boxes; resolver determinism |
| Collaborative Memory ([2505.18279](https://hf.co/papers/2505.18279)) | provenance + dynamic access control, auditability | provenance (§3.1), context enforcement |
| Graph-based Agent Memory survey ([2602.05665](https://hf.co/papers/2602.05665)) | taxonomy of graph memory | box/context graph |
| MemoryGraft ([2512.16962](https://hf.co/papers/2512.16962)) | **poisoned-retrieval attack → behavioral drift** | the threat the trust score defends against |
| Benchmarks | LongMemEval, LoCoMo, AMA-Bench ([2602.22769](https://hf.co/papers/2602.22769)), MemoryAgentBench ([2507.05257](https://hf.co/papers/2507.05257)) | targets for `fabric_rag_bench.py` |

## Where the fabric already aligns

- **Typed memory** (Memanto) → boxes are typed by kind-boxes; retrieval is
  deterministic and resolvable.
- **Provenance + access control** (Collaborative Memory) → provenance on every box
  (§3.1), context-enforced access (§1.4), audit by change feed.
- **Graph memory** (survey, Mem0g) → boxes-in-context graph, node+box resolution.
- **Anti-poisoning** (MemoryGraft) → trust filter (ratified + resolved +
  provenance-pinned) is the direct countermeasure to drift; the Agent GPA marks
  poisoned/drifting agents down (`fabric-agent-scoring.md`).

## The gap we adopted: bi-temporal validity

The frontier (Graphiti/Zep/RoMem) makes facts **time-bounded**. The fabric now
carries `valid_from` / `valid_to` per box and a temporal query
`Graph.as_of(t)` (`scripts/fabric_model.py`), answering *"what did the agent
believe at time T."* Demonstrated:

```
as_of t=5   budget owner -> ['alice']
as_of t=15  budget owner -> ['bob']
```

Next steps (not yet done): a **temporal resolver** (`resolve as_of T` — the graph
must resolve at every point in time), and running `fabric_rag_bench.py` against
**LongMemEval / LoCoMo** for comparability.

## Positioning

The fabric's novelty vs. the above is the **uniform, self-describing, resolvable**
treatment: memory, model, governance, and trust scoring are one box graph that
must resolve at node + box. Temporal validity slots in as another field on the
same box — *one model, now time-aware.*
