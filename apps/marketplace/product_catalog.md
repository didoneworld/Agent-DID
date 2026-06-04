# 📦 Agent-DID Product Catalog

This catalog defines **products as graph-native capabilities**, not traditional e-commerce items.

---

# 🧠 Core Principle

> A product is a **capability node in the identity graph**.

It is not a SKU.
It is not a listing.

It is:

```
Agent / Service → offers → Capability(Product)
```

---

# 🧬 Product Model

## Product Node

```json
{
  "id": "string",
  "type": "product",
  "name": "string",
  "category": "string",
  "capabilities": ["string"],
  "metadata": {}
}
```

---

## Product Edge Types

- `offers` → Agent provides product
- `consumes` → Agent uses product
- `depends_on` → Product requires another product
- `trusts` → Product is trusted by agent graph

---

# 🛒 Catalog Structure

## 1. Compute Products
- AI agents
- inference services
- data processing pipelines

## 2. Identity Products
- DID issuance
- verification services
- authentication agents

## 3. Trust Products
- reputation scoring
- validation services
- attestation agents

## 4. Data Products
- graph queries
- datasets
- event streams

## 5. Execution Products
- workflow agents
- automation services
- API executors

---

# 🔍 Product Discovery

Products are discovered via graph traversal:

```
user → can_act → agent → offers → product
```

or

```
user → trust_path → provider → product
```

---

# 🔐 Marketplace Constraint

A product is valid only if:

- It exists as a graph node
- It is reachable via trust or delegation path
- It satisfies policy constraints (future layer)

---

# ⚡ Key Shift

Traditional marketplace:
- search → list → buy

Agent-DID marketplace:
- traverse → reason → access

---

# 🚀 Future Extensions

- reputation graph weighting
- pricing as edge property
- dynamic capability composition
- agent-to-agent product synthesis

---

# 🧠 Summary

> Products are not items. They are **reachable capabilities in an identity graph**.
