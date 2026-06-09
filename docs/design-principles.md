# Agent DID — Design Principles

This document defines the core **design principles** that govern the Agent DID system. These principles ensure the system remains cloud-native, vendor-neutral, secure, and scalable for both human and autonomous agent identity.

> **Constitutional frame.** The principles below are *statutes* — concrete
> technical commitments. They are derived under a higher-order, constitutional
> frame: [**The Fabric of Work**](./fabric-of-work.md), which defines how
> meaning, work, and governance are legitimately established. Where a principle
> here and that document conflict in spirit, resolve it by re-derivation under
> the constitution, not by decree.

---

# 1. Identity is Cryptographic, Not Declarative

All identities (humans, agents, services) are rooted in cryptographic primitives:

- Decentralized Identifiers (DIDs)
- Public/private key ownership
- Verifiable credentials (VCs)

> Identity is something you prove, not something you request.

---

# 2. Control Plane Must Be Stateless

The Agent DID API layer is stateless by design.

- No session dependency in core services
- State lives in Postgres / graph database
- Horizontal scaling is always safe

---

# 3. Vendor Neutrality is Mandatory

The system must never depend on a single cloud provider:

Forbidden dependencies:
- AWS IAM
- Azure AD
- Google Identity Platform

Allowed primitives:
- OIDC
- SAML
- SCIM
- SPIFFE
- DID standards

---

# 4. Identity is a Graph, Not a Table

Identity is modeled as a graph structure:

- Nodes: users, agents, services, organizations
- Edges: delegation, trust, ownership, membership

This enables:
- cross-system resolution
- identity fusion
- delegation chains

---

# 5. Authentication and Authorization Must Be Separated

- Authentication answers: **Who are you?**
- Authorization answers: **What can you do?**

They must never be mixed in business logic.

---

# 6. Policy is Externalized

All authorization decisions must go through a policy engine:

- Casbin (RBAC / ABAC)
- or FGA-style relationship graph rules

No hardcoded permission checks in application code.

---

# 7. Runtime Identity Must Be Ephemeral

Execution-time identity is short-lived and dynamically issued:

- SPIFFE-style workload identity
- mTLS certificates with rotation
- zero long-lived secrets in runtime

---

# 8. Everything is API-First

Every capability is exposed via stable APIs:

- /identity
- /agent-records
- /authorize
- /audit
- /policy

All UIs and CLIs are clients of these APIs.

---

# 9. Governance is First-Class

Identity is not just technical—it is governed:

- lifecycle states (active, suspended, revoked)
- approval workflows
- audit trails
- compliance hooks

---

# 10. Composability Over Monoliths

Each subsystem must remain independently replaceable:

- Identity (DID layer)
- Authorization (Casbin / FGA)
- Runtime identity (SPIFFE)
- Storage (Postgres / Graph DB)

No hard coupling between layers.

---

# 11. Multi-Agent Ready by Default

The system assumes:

- multiple autonomous agents per organization
- agent-to-agent delegation
- hierarchical and peer trust relationships

---

# 12. Observability is Mandatory

Every identity and authorization decision must be traceable:

- audit logs
- decision traces
- policy evaluation visibility

---

# 13. Failure is Explicit

No silent failures:

- all authorization failures must return deterministic responses
- ambiguity is not allowed in policy evaluation

---

# 14. Security by Design

- zero trust architecture
- least privilege enforcement
- short-lived credentials
- signed identity assertions

---

# Vision

Agent DID is designed to become a:

> Cloud-native, vendor-neutral identity control plane for humans and autonomous agents across all infrastructure.

---
