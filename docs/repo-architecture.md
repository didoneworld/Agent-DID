# Agent DID — Repository Architecture

This document defines the **cloud-native, vendor-neutral architecture** for the Agent DID system.

It describes how identity, authorization, governance, and runtime identity are separated into composable layers.

---

# 🧠 System Overview

Agent DID is designed as a **distributed Identity Control Plane for AI agents and humans**.

It follows a strict separation of concerns:

```
Identity (WHO you are)
    ↓
Authorization (WHAT you can do)
    ↓
Runtime Identity (HOW you execute securely)
    ↓
Infrastructure (WHERE it runs)
```

---

# 🏗️ Monorepo Structure

```
agent-did/
│
├── apps/
│   ├── web/                      # Next.js dashboard (Admin + Control UI)
│   ├── api/                      # FastAPI control plane (core system)
│   └── cli/                     # CLI for operators and automation
│
├── core/
│   ├── identity/                # DID engine (agent + human identities)
│   ├── registry/                # Agent record store + lifecycle
│   ├── governance/              # policies, approvals, audit rules
│   └── events/                  # event bus (identity + audit events)
│
├── authz/
│   ├── casbin/                 # RBAC / ABAC policy engine integration
│   ├── fga/                    # relationship-based authorization graph
│   └── policies/               # tenant policies (declarative)
│
├── runtime/
│   ├── spiffe/                # SPIFFE/SPIRE integration layer
│   ├── mtls/                  # certificate issuance + rotation
│   └── workload-identity/     # agent runtime identity binding
│
├── identity-fabric/           # cross-system identity graph engine
│   ├── resolvers/             # Google, GitHub, SSO connectors
│   ├── enrichment/            # profile aggregation
│   └── graph/                 # identity relationship store
│
├── integrations/
│   ├── oidc/                  # OpenID Connect provider integration
│   ├── saml/                  # enterprise SAML integration
│   ├── scim/                  # provisioning/deprovisioning
│   └── webhooks/              # external system events
│
├── storage/
│   ├── postgres/              # primary relational store
│   ├── surrealdb/             # identity graph / relationships
│   └── cache/                 # redis or equivalent
│
├── infra/
│   ├── docker/                # container definitions
│   ├── kubernetes/            # K8s manifests
│   ├── helm/                  # Helm charts
│   └── terraform/            # cloud provisioning (vendor-neutral)
│
├── sdk/
│   ├── python/               # Python SDK for agents
│   ├── ts/                   # TypeScript SDK for web apps
│   └── go/                   # optional runtime SDK
│
├── docs/
│   ├── how-to-guide.md
│   ├── product-documentation.md
│   ├── agent-id-spec.md
│   └── repo-architecture.md
│
└── site/
    ├── index.html            # GitHub Pages landing page
    └── styles.css
```

---

# ☁️ Cloud-Native Principles

## 1. Stateless Control Plane
All APIs in `apps/api` are stateless.
State lives in Postgres / graph DB.

---

## 2. Vendor Neutrality
No dependency on:
- AWS IAM
- Azure AD
- GCP Identity Platform

Instead:
- OIDC
- SAML
- SPIFFE
- DID

---

## 3. Identity as a Graph
Identity is not a table.
It is a graph:

- users
- agents
- services
- relationships
- delegation edges

---

## 4. Policy-Driven Authorization
All access decisions flow through:

- Casbin (RBAC/ABAC)
- FGA graph rules

No hardcoded permissions.

---

## 5. Runtime Identity Binding
At execution time:

- SPIFFE issues workload identity
- short-lived mTLS certs
- zero static secrets

---

# 🔐 Core System Flow

```
User / Agent
    ↓ (OIDC / SAML / API Key)
Auth Layer (apps/api)
    ↓
Agent DID Registry
    ↓
Authorization Engine (Casbin / FGA)
    ↓
Policy Decision
    ↓
Runtime Identity (SPIFFE)
    ↓
Secure Execution (mTLS)
```

---

# 🧩 Key Modules Explained

## Identity Core
- DID generation
- agent registry
- lifecycle state (active, suspended, deprovisioned)

## Authorization Layer
- RBAC (Casbin)
- relationship-based access (FGA)
- policy versioning per tenant

## Identity Fabric
- resolves external identities
- builds cross-platform graph
- enriches identity metadata

## Runtime Layer
- SPIFFE identity issuance
- workload identity binding
- mTLS enforcement

---

# 🚀 Deployment Model

Supports:
- Docker Compose (local)
- Kubernetes (production)
- Hybrid (edge + cloud)

---

# 🌍 Vision

Agent DID is designed to become:

> A vendor-neutral identity control plane for humans, services, and autonomous agents across all infrastructure.

---
