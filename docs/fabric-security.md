# Fabric Security — OWASP LLM Top 10, Supply Chain, CSA Alignment

> Derived, contestable (`fabric-of-work.md` §12). Maps the fabric's built-in
> controls to established frameworks. **Caveat:** this is a control mapping at the
> category level; exact control-ID cross-walks to the cited frameworks are future
> work.

## OWASP Top 10 for LLM Applications (2025) → fabric controls

| OWASP LLM risk | Fabric control |
|---|---|
| **LLM01 Prompt injection** | untrusted input enters as `realm:digital` sandbox boxes; never auto-promoted; commands are typed/validated and **context-enforced** (§1.4) |
| **LLM02 Sensitive info disclosure** | context-scoped access, row-level security, **air-gapped** option (§9), least privilege |
| **LLM03 Supply chain** | AI registry: artifacts are boxes with **provenance + ratification + resolution**; pinned sources; minimal deps (one box type) — see below |
| **LLM04 Data / model poisoning** | **trust filter** (ratified + resolved + provenance-pinned); promotion gated; defends MemoryGraft-style drift |
| **LLM05 Improper output handling** | schema validation on egress; **failure is explicit** (§7.5); no silent drift |
| **LLM06 Excessive agency** | capability/command boxes **scoped to context**; ratify gates; constraints (§7); bounded blast radius |
| **LLM07 System-prompt leakage** | prompts are boxes with access control; air-gap; context isolation |
| **LLM08 Vector / embedding weaknesses** | trust-filtered retrieval; provenance on memory; context-scoping shrinks the poisoning surface |
| **LLM09 Misinformation** | meaning is **derived, contestable, re-derivable** (§3.5); resolution blocks unfounded claims |
| **LLM10 Unbounded consumption** | quotas/constraints (§7); per-tenant isolation; rate limits |

## Open-source supply-chain risk (LLM03, expanded)

The fabric treats the **model/dataset/prompt/dependency supply chain as governed
boxes** (the AI registry, `fabric-use-cases.md` §3):

- **Provenance-pinned sources** — every artifact box pins its origin (§3.1);
  unpinned provenance raises the agent **risk score** (`fabric-agent-scoring.md`).
- **Ratify + resolve gates** — an artifact is `stable`/`real` only after it
  resolves (node + box) and is ratified (§3.3) — no unverified dependency goes
  live.
- **Minimal surface** — one box type, schemafull envelopes, no out-of-band schema
  engine (`fabric-substrate.md` §5.2) → small dependency and attack footprint.
- **SBOM-as-graph** — the dependency graph *is* boxes + `derives` edges; a
  supply-chain audit is a graph resolution, and a compromised dependency is a
  box whose provenance fails to resolve.
- **Air-gapped / local LLM** removes external fetch entirely
  (`fabric-substrate-comparison.md`).

## Constraint enforcement: OpenFGA (pure, relationship-based)

The constraint layer (§7) and externalized policy (`design-principles.md` §6) are
enforced with **OpenFGA** — open-source, Zanzibar-style **relationship-based access
control (ReBAC)** — because authorization in the fabric is already a **graph
question**.

- **Authorization = reachability.** "May agent A perform construction C in context
  X?" is "does a *permitted* relationship path exist?" OpenFGA tuples map 1:1 onto
  the fabric's relations (`fills`, `contains`, `commands`, `performs`,
  `instance_of`); a check is node resolution restricted to permitted edges.
- **Pure constraints — constraints as data, not code.** No hardcoded permission
  logic anywhere; every constraint is a relationship tuple evaluated by OpenFGA.
  This *is* "policy is externalized" (§6) and the constraint face of structure
  (§7): the box graph carries both the work and the rules over it.
- **Constraints stay resolvable.** Because a permission is just a typed edge, an
  authorization decision participates in node/box resolution — an unauthorized or
  dangling permission edge is an explicit failure (§7.5), not a silent allow.
- **Open agents.** Interop via open agent protocols (A2A, ACP, ANP, MCP) and W3C
  DID/VC: an agent presents verifiable relationships; OpenFGA enforces them
  uniformly across the federation (§3.7), no central policy owner (§3.4).

## CSA framework alignment

The fabric's controls are intended to align with Cloud Security Alliance guidance:

- **AI Controls Matrix (AICM)** — governance, data security, model security, and
  runtime controls map to: derived/ratified governance (§3), context-enforced
  data access (§1.4), provenance + resolution for model integrity, and
  least-privilege runtime (§9).
- **STAR for AI** — the fabric's **provenance + resolution + scorecard** provide
  the auditable evidence a STAR-style assurance/attestation needs (trust is
  computed, not asserted).
- **2026 State of Modern Application and AI Security** — the fabric directly
  targets its themes: supply-chain integrity, agent trust, and drift resistance.

Sources: [CSA AI Controls Matrix](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix),
[CSA STAR for AI](https://cloudsecurityalliance.org/star/ai/),
[CSA 2026 State of Modern Application and AI Security](https://cloudsecurityalliance.org/artifacts/2026-state-of-modern-application-and-ai-security),
[OWASP Top 10 for LLM Applications](https://genai.owasp.org/).

## Summary

Security in the fabric is **structural, not bolted on**: federated provenance +
node/box resolution + context enforcement + trust scoring cover the OWASP LLM Top
10 and supply-chain risk by construction, and produce the auditable evidence CSA
frameworks expect. The most secure configuration is **air-gapped + local LLM +
pinned provenance** — minimal ingress, maximal trust.
