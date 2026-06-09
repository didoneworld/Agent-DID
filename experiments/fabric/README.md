# Fabric Experimentation Environment — SurrealDB Backend

This is the constitution's **experimentation environment** (sandbox / virtual box,
[`../../docs/fabric-of-work.md`](../../docs/fabric-of-work.md) §8.4.2) made real on
**SurrealDB as the backend (BE + DB)**.

> **SurrealDB is the building base / backend — *not* the runtime.** The runtime
> (the fabric / OS for work, §5, §9.3) executes *above* this store. State lives in
> SurrealDB; the control plane stays stateless (`design-principles.md` §2).

## Files

| File | Role |
|---|---|
| `schema.surql` | backend schema — `box` (SCHEMAFULL envelope + FLEXIBLE payload), `context`, RELATION edge tables |
| `seed.surql` | the stable-state kernel (the model is the graph) + a sample construction |
| `resolve.surql` | in-database validation: node → real, box → stable |
| `run_backend.py` | provisions SurrealDB (Docker → local binary → reference fallback), loads, resolves |
| `test_backend.py` | testcontainer-style test (skips without Docker) + always-on reference test |

## Run

```bash
# Uses a SurrealDB Docker image if available (testcontainer style), else a local
# `surreal` binary, else validates the identical kernel via the in-process model.
python3 experiments/fabric/run_backend.py

# Testcontainer-style test (auto-skips if no Docker/surreal):
pytest experiments/fabric/test_backend.py -v
```

The Docker path runs `surrealdb/surrealdb` (`start --mem`), loads `schema.surql`
+ `seed.surql`, and runs `resolve.surql` against the live instance.

## Design notes

- **First, fit the real world.** The sandbox is digital-only (`realm = 'digital'`,
  §8.4); a construction is **promoted** to `realm = 'real'` only after it (a)
  resolves at node + box and (b) is ratified (§3.3). The digital model must
  *correspond to* the real world before it is allowed to act on it (§8.4.3) — the
  seam between digital and real is governed.
- **JSON-LD.** `context` is the JSON-LD `@context` of the fabric (§3, §10.4):
  meaning and value are derived *in* a context. A box serializes to JSON-LD by
  emitting its `payload` under its `context`'s `@context`, so the same box is
  linked data on the wire and a graph node in the store — *data-in-context*,
  portable across the Internet of Agents (§3.7).
- **Validity = the resolver, in the store.** `resolve.surql` is the SurrealQL form
  of `scripts/fabric_graph.py` / `scripts/fabric_model.py`: the constitution
  checks itself inside its own backend.
