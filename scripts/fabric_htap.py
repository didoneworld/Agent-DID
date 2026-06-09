#!/usr/bin/env python3
"""HTAP test — transactional AND analytical workloads on one box graph.

Agentic work needs both:
  * transactional (OLTP): point reads/writes of boxes, ACID, real-time (§6.1).
  * analytical   (OLAP): rollups over the graph — value/cost/score aggregates,
                  counts by state/kind/context (§6.3 measurable).

Both run over the same boxes-in-context. On a real backend this is HTAP
(SingleStore / OceanBase), or split OLTP (SurrealDB) + OLAP (ClickHouse) fed by
the change feed. Here we show both over the in-process model.
"""
from __future__ import annotations

import random
import time


def build(n: int, contexts: int = 8, kinds=("agent", "command", "construction",
                                            "ingredient", "tool"), seed=4):
    rnd = random.Random(seed)
    states = ("proposed", "ratified", "stable", "revoked")
    boxes = {}
    for i in range(n):
        boxes[i] = {
            "ctx": i % contexts,
            "kind": rnd.choice(kinds),
            "state": rnd.choices(states, weights=(1, 2, 6, 1))[0],
            "value": rnd.randint(0, 100),
            "cost": round(rnd.random() * 10, 2),
        }
    return boxes


def main() -> int:
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    boxes = build(n)
    rnd = random.Random(1)
    print("=" * 60)
    print(f"FABRIC HTAP TEST  (n={n:,} boxes)")
    print("=" * 60)

    # ---- OLTP: point reads + updates ------------------------------------
    ops = 20_000
    t = time.perf_counter()
    acc = 0
    for _ in range(ops):
        i = rnd.randrange(n)
        acc += boxes[i]["value"]           # point read
        boxes[i]["value"] += 1             # point update (transactional)
    dt = time.perf_counter() - t
    print(f"[OLTP] {ops:,} point read+update ops in {dt*1000:6.1f} ms "
          f"-> {2*ops/dt:,.0f} ops/s")

    # ---- OLAP: analytical rollups ---------------------------------------
    t = time.perf_counter()
    value_by_ctx: dict = {}
    cost_by_kind: dict = {}
    count_by_state: dict = {}
    for b in boxes.values():
        value_by_ctx[b["ctx"]] = value_by_ctx.get(b["ctx"], 0) + b["value"]
        cost_by_kind[b["kind"]] = cost_by_kind.get(b["kind"], 0.0) + b["cost"]
        count_by_state[b["state"]] = count_by_state.get(b["state"], 0) + 1
    dt = time.perf_counter() - t
    print(f"[OLAP] full-scan rollups (value/ctx, cost/kind, count/state) "
          f"in {dt*1000:6.1f} ms -> {n/dt:,.0f} rows/s")
    print("-" * 60)
    print("  value by context :", {k: value_by_ctx[k] for k in sorted(value_by_ctx)})
    print("  cost  by kind    :", {k: round(v, 1) for k, v in sorted(cost_by_kind.items())})
    print("  count by state   :", dict(sorted(count_by_state.items())))
    print("-" * 60)
    print("one box graph serves OLTP (point CRUD, ACID) and OLAP (rollups).")
    print("backend: HTAP (SingleStore/OceanBase) or OLTP+OLAP split via change feed.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
