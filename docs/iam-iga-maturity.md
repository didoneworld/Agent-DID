# IAM + IGA Maturity Model (for Agent Identity)

> A staged maturity model for **Identity & Access Management (IAM)** and **Identity
> Governance & Administration (IGA)**, specialized for *agent* identity, with an
> honest placement of where Agent DID / Agent OS is **stable**, **MVP**, or
> **planned**. Derived, contestable (`fabric-of-work.md` §12).

## The five levels

| Level | Name | IAM characteristics | IGA characteristics |
|---|---|---|---|
| **L1** | Ad hoc | shared keys, manual auth, no central identity | none — access is undocumented |
| **L2** | Managed | central authN (OIDC/SAML), API keys, sessions | basic lifecycle (create/disable), audit log |
| **L3** | Defined | federation, standards‑based authZ, provisioning (SCIM) | defined lifecycle states, approval workflows, policy externalized |
| **L4** | Governed | continuous signals (revocation/CAEP), least privilege enforced | access **certification/attestation**, segregation of duties, full audit, provenance |
| **L5** | Optimized | risk‑adaptive, just‑in‑time, ephemeral identity | **analytics‑driven** governance: trust scoring, drift detection, automated remediation |

## Dimensions

**IAM** — Authentication · Authorization · Federation · Provisioning · Runtime
identity.
**IGA** — Lifecycle · Approval/workflow · Certification (attestation) · Segregation
of Duties (SoD) · Audit · Identity analytics.

## Where Agent DID / Agent OS stands

Legend: ✅ **stable** · ◐ MVP · ○ planned

### IAM

| Dimension | Capability | Status |
|---|---|---|
| Authentication | OIDC discovery, JWKS, OAuth2.1/PKCE, token, introspection (7662), revocation (7009) | ✅ stable |
| Authentication | SAML SP (signed metadata, assertion checks) | ✅ stable |
| Authentication | sessions, API keys (HMAC) | ✅ stable |
| Authorization | AuthZEN PEP + relationship (ReBAC/OpenFGA) tuples | ◐ MVP |
| Federation | DID‑anchored agent identity; Internet‑of‑Agents protocol | ◐ MVP / ○ |
| Provisioning | SCIM 2.0 `AgenticIdentity` CRUD | ✅ stable |
| Runtime identity | ephemeral / SPIFFE‑style workload identity | ○ planned |

→ **IAM ≈ Level 3 (Defined), stabilizing toward L4.**

### IGA

| Dimension | Capability | Status |
|---|---|---|
| Lifecycle | states (active/suspended/revoked), deprovisioning, blueprints | ◐ MVP |
| Approval / workflow | approval gate | ◐ MVP |
| Certification / attestation | periodic access recertification of agents | ○ planned |
| Segregation of Duties | conflicting‑capability detection | ○ planned |
| Audit | append‑only audit events, provenance on every box | ✅ stable (provenance) / ◐ |
| Identity analytics | **trust scoring (GPA), risk/threat profile, drift detection** | ✅ stable (fabric) |

→ **IGA ≈ Level 2–3 today; the fabric supplies the Level‑5 analytics layer
(trust scoring, drift resistance) ahead of the L4 governance plumbing.**

## What makes the model *stable*

The maturity model is **anchored to a computable invariant**, not subjective
audit: every identity, permission, and certification is a box that must **resolve
at node + box**. That gives each level a falsifiable test:

- **L3 stable** when provisioning + federation resolve (no dangling identities or
  permissions).
- **L4 stable** when certifications and SoD rules are boxes whose violations are
  *explicit failures* (§7.5), and revocation streams in real time (CAEP).
- **L5 stable** when trust/risk scores are computed from resolvable, provenance‑
  bearing data (already true — `fabric-agent-scoring.md`).

## Roadmap to L4/L5 (governed + optimized)

1. **Certification/attestation** — recurring access reviews as ratified boxes.
2. **Segregation of Duties** — SoD as relationship constraints (OpenFGA), violations
   as explicit failures.
3. **Continuous revocation** — promote the SSF/CAEP emitter from MVP to enforced.
4. **Just‑in‑time / ephemeral identity** — SPIFFE‑style runtime credentials.
5. **Closed‑loop remediation** — drift/risk score crossing a threshold auto‑opens a
   governance action.

> Net: **IAM is stable at L3**; **IGA analytics (trust/drift) is stable at L5**; the
> gap to close is the **L4 governance plumbing** (certification, SoD, enforced
> continuous revocation). Each milestone is *done* when its boxes resolve.
