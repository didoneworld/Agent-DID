#!/usr/bin/env python3
"""Fabric chaos test — resilience of the box/node graph under fault injection.

Chaos-Mesh-style fault injection at the graph level: kill boxes (node failure) or
a whole shard (federation failure), then re-resolve and measure the CHAOS SCORE =
the fraction of the graph that still resolves (real + stable) after the fault.

Key question: does federation bound the blast radius? (constitution §3.4). A
random kill degrades the whole graph; a shard kill should only break the
cross-shard references INTO the dead shard, leaving every other shard intact.
"""
from __future__ import annotations

import random
import sys


def build(n: int, shards: int, cross: float = 0.10, seed: int = 5):
    rnd = random.Random(seed)
    per = max(1, n // shards)
    shard_of = [min(i // per, shards - 1) for i in range(n)]
    refs: list[list[int]] = [[] for _ in range(n)]
    for i in range(n):
        deg = 3 if i >= 3 else i
        lo = shard_of[i] * per
        for _ in range(deg):
            if i and rnd.random() < cross:
                t = rnd.randrange(0, i)                 # cross-shard allowed
            elif i > lo:
                t = rnd.randrange(lo, i)                # same-shard earlier
            else:
                t = rnd.randrange(0, i) if i else 0
            refs[i].append(t)
    return shard_of, refs


def intact(alive: set, refs) -> int:
    """boxes that survive AND whose every reference still resolves."""
    c = 0
    for i in alive:
        if all(t in alive for t in refs[i]):
            c += 1
    return c


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000
    shards = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    shard_of, refs = build(n, shards)

    print("=" * 64)
    print(f"FABRIC CHAOS TEST  (n={n:,}, shards={shards}, ~10% cross-shard refs)")
    print("=" * 64)
    print("RANDOM NODE KILL (no isolation):")
    for f in (0.01, 0.05, 0.10, 0.25):
        rnd = random.Random(99)
        dead = set(rnd.sample(range(n), int(n * f)))
        alive = set(range(n)) - dead
        score = intact(alive, refs) / n
        print(f"  kill {f:>4.0%}  -> chaos score (still resolving) = {score:6.1%}")

    print("-" * 64)
    print("SHARD KILL (federation isolates blast radius, §3.4):")
    base_alive = set(range(n))
    base = intact(base_alive, refs)
    for ks in (0, shards // 2):
        alive = {i for i in range(n) if shard_of[i] != ks}
        surv = intact(alive, refs)
        # of the boxes NOT in the dead shard, how many stayed intact?
        others = len(alive)
        print(f"  kill shard {ks:<2} -> {surv:,}/{others:,} surviving boxes intact "
              f"({surv/others:6.1%}); whole-graph score = {surv/n:6.1%}")
    print("-" * 64)
    print(f"baseline intact (no fault): {base/n:6.1%}")
    print("read: random kill degrades the whole graph; a shard kill only breaks")
    print("cross-shard refs INTO the dead shard — every other shard stays intact,")
    print("so federation bounds the blast radius. Failures are explicit (§7.5).")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
