# Agent Scoring — Trust, Reliability, Usability, GPA, Risk

> Derived, contestable (`fabric-of-work.md` §12). Implemented in
> `scripts/fabric_agent_score.py`.

In the fabric an agent is a box; its memory, constructions, and provenance are
boxes and edges (§10). So an agent's quality is **computed from resolvable,
provenance-bearing data**, not asserted.

## Metrics (each in [0,1])

| Metric | Definition | Anchors |
|---|---|---|
| **Trust** | share of memory that is ratified + resolved + provenance-bearing | §3.1, §3.3 |
| **Reliability** | share of constructions that resolved (real + stable) vs refused/drift | §7.5 |
| **Usability** | trusted recall at real-time latency = `recall@k × responsiveness` | §10.5 |

`responsiveness = min(1, target_ms / latency_ms)`; latency spans ingress→egress.

## Agent GPA

Composite on a 0.0–4.0 scale with a letter grade:

```
GPA = 4.0 × (0.40·Trust + 0.35·Reliability + 0.25·Usability)
```

**Trust is weighted highest** — for agents it is the binding constraint: low trust
caps the GPA no matter how fast or accurate the agent is. This is the structural
defense against **AI drift**: an agent that answers fast but on untrusted,
unresolved memory cannot score well.

## Risk & threat profile (lower is better)

```
Risk = 0.35(1−Trust) + 0.25(1−Reliability) + 0.20·ingress_exposure + 0.20(1−source_pinned)
```

Levels: Low `<0.15` · Moderate `<0.35` · Elevated `<0.60` · High. Threats are the
risk drivers that cross threshold:

| Driver | Threat |
|---|---|
| low trust | memory poisoning / untrusted recall |
| **unpinned provenance** | drift (sources not pinned) |
| low reliability | construction drift / instability |
| ingress exposure | exfiltration / tampering |
| high latency | real-time DoS |

**"Pin sources":** every memory box should pin its provenance source (§3.1).
Pinned sources lower risk and resist drift; air-gapped deployment (ingress = 0)
removes a whole risk term.

## Example (computed)

| Agent | Trust | Reliab | Usable | GPA | Grade | Risk |
|---|---|---|---|---|---|---|
| alice (mature) | 97% | 98% | 97% | 3.89 | A | 0.03 Low |
| carol (new) | 97% | 100% | 91% | 3.86 | A | 0.04 Low |
| bob (drifting) | 60% | 65% | 34% | 2.21 | C+ | 0.44 Elevated |

## Relation to task benchmarks (SWE-bench etc.)

Task-success benchmarks (e.g. SWE-bench) measure *did it solve the task*. That is
**necessary but not sufficient** for an agent in the fabric. The GPA adds the
dimensions task-success ignores: *is the agent's memory trusted, does its work
resolve, is it drift-resistant, what is its risk?* An agent can pass tasks while
poisoning its memory or drifting — and the scorecard will mark it down. Task
success feeds **Usability/Reliability**; trust and risk are the fabric's addition.
