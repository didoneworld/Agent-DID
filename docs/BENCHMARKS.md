# Fabric Benchmarks — Public Results

> Deterministic, offline, reproducible. **Reproduce all:**
> `bash scripts/run_benchmarks.sh`
>
> Environment caveat: results below are single-machine, pure-Python (no numpy),
> and synthetic; 8e9 figures are modeled extrapolations; database engines were not
> benchmarked head-to-head (unavailable). Numbers vary with hardware.

## Summary

| # | Benchmark | Script | Headline result |
|---|---|---|---|
| 1 | Constitution resolution | `fabric_graph.py` | 80 boxes, **NODE real, BOX stable → VALID** (0 dangling) |
| 2 | Self-describing model | `fabric_model.py` | 26 boxes, **VALID**; JSON-LD, promotion, live stream, bi-temporal |
| 3 | Resolution scale | `fabric_scale_bench.py` | **~23.5M elems/s/core, linear**; 8e9 → ~160 federated shards |
| 4 | Retrieval (RAG/memory/trust) | `fabric_rag_bench.py` | memory (context-scoped) **3.7× faster** than global RAG at **100%** precision@5 |
| 5 | Agent scorecard | `fabric_agent_score.py` | mature **3.89 (A)**, drifting **2.21 (C+, Elevated risk)** |
| 6 | Chaos / resilience | `fabric_chaos.py` | random 10% kill → **66%**; **shard kill → 92–98%** survivors intact |
| 7 | Backend resolution | `run_backend.py` | **VALID** on SurrealDB (or in-process reference fallback) |

## Detail

**1. Constitution resolution.** Parses `docs/fabric-of-work.md` into 80 boxes / 94
references; every reference resolves (node→real), every box is filled, placed, and
typed (box→stable). **VALID (real + stable).**

**2. Self-describing stable-state model.** 26 boxes (13 kinds, 7 relations, 6
data); every box typed by a box, every edge related by a box, self-typed fixpoint
`kind:kind`. VALID. Demonstrates JSON-LD serialization, gated digital→real
promotion, real-time streaming, and bi-temporal `as_of(t)` (`t=5 → alice`,
`t=15 → bob`).

**3. Resolution scale.** 100k/1M/3M boxes resolve at ~23.5M elements/s/core,
linear; node-real + box-stable held throughout. 8×10⁹ ≈ 584 GB → ~160 shards of
50M (~3.6 GB, ~10–12 s each, parallel ≈ same wall-clock).

**4. Retrieval.** 8,000 boxes, dim 16, exact search: RAG (global) 88 q/s,
precision@5 = 100%; **AI memory (context-scoped) 322 q/s (3.7×), 100%**; trust
(ratified-only) 106 q/s, 100% trusted. Context-scoping wins on speed at equal
accuracy.

**5. Agent scorecard.** Trust/Reliability/Usability → GPA (0–4, trust weighted
highest) + risk/threat: alice 3.89 (A, Low 0.03), carol 3.86 (A, Low 0.04), bob
(drifting) 2.21 (C+, Elevated 0.44, threats listed).

**6. Chaos / resilience.** Random kill: 1%→96%, 5%→81%, 10%→66%, 25%→32%. **Shard
kill: 92–98% of surviving boxes intact** → federation bounds blast radius.

## Alignment with public benchmarks

The fabric's synthetic harnesses are designed to be re-pointed at standard public
benchmarks for comparability (future work):

| Public benchmark | Maps to fabric metric |
|---|---|
| LongMemEval, LoCoMo | retrieval recall / temporal memory (`fabric_rag_bench.py` + `as_of`) |
| AMA-Bench, MemoryAgentBench | long-horizon memory competencies |
| SWE-bench, HF Coding Agent Leaderboard | Usability/Reliability feed into Agent GPA |
| OWASP LLM Top 10, CSA AICM/STAR | security controls (`fabric-security.md`) |

## Reproduce

```bash
bash scripts/run_benchmarks.sh          # all of the above
python3 scripts/fabric_graph.py         # any single benchmark
```
