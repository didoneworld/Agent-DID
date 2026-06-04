# 🛒 Agent-DID Marketplace

This module turns Agent-DID into a **trust-aware identity marketplace** where agents, services, and users can publish and consume capabilities through the identity graph.

---

# 🧠 Core Idea

The marketplace is NOT a traditional e-commerce system.

It is a **graph-native exchange layer** where:

- Nodes = Agents / Services / Users
- Edges = Trust / Delegation / Capability relationships
- Listings = Claims published by identity nodes
- Transactions = Graph-mediated interactions

---

# ⚙️ Core Concepts

## 1. Listing (Offer)
A capability exposed by an agent/service.

Example:
- "data-cleaning-agent"
- "image-generation-service"
- "auth-delegation-capability"

---

## 2. Request (Intent)
A consumer node requesting a capability.

---

## 3. Match
A graph traversal process:

```
consumer → can_act → provider → capability match
```

---

## 4. Trust Constraint
A transaction is valid only if:

- `can_act(consumer, provider) == True`
- AND capability exists

---

# 🧬 Marketplace Model

```
Agent (node)
   ↓ offers
Capability (edge/property)
   ↓ consumed by
Another Agent (node)
```

---

# 🔐 Key Feature

Unlike normal marketplaces:

> Access is not granted by payment, but by graph reachability.

---

# 🚀 Future Extensions

- Reputation graph
- Capability scoring
- Token-less exchange layer
- Policy-driven marketplace filters

---

# ⚡ Status

This is a **graph-native trust marketplace prototype** built on Agent-DID.
