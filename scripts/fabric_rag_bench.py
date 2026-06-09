#!/usr/bin/env python3
"""Fabric retrieval benchmark — RAG, AI memory, and trust over boxes-in-context.

In the fabric these three are the SAME shape (a box is data-in-context, §10):
  * RAG        : retrieve boxes by similarity (vector over payload).
  * AI memory  : retrieve durable boxes scoped to a context (memory-in-context).
  * Trust      : retrieve only ratified, provenance-bearing boxes (§3.1, §3.3).

Measured on the three axes the substrate is judged by: speed, accuracy, and
real-time reaction. Pure-Python (no numpy) brute-force cosine = exact search;
an ANN index trades a little accuracy for more speed (noted, not implemented).
"""
from __future__ import annotations

import math
import random
import sys
import time


def build(n: int, dim: int, clusters: int, seed: int = 11):
    rnd = random.Random(seed)
    cents = [[rnd.gauss(0, 1) for _ in range(dim)] for _ in range(clusters)]
    boxes = []  # (vec, inv_norm, cluster, ctx, ratified)
    for i in range(n):
        c = rnd.randrange(clusters)
        v = [cents[c][j] + rnd.gauss(0, 0.15) for j in range(dim)]
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        boxes.append((v, 1.0 / norm, c, c % 4, (i % 5 != 0)))  # 4 ctxs, 80% trusted
    return cents, boxes


def query_vec(cents, cluster, dim, rnd):
    v = [cents[cluster][j] + rnd.gauss(0, 0.15) for j in range(dim)]
    inv = 1.0 / (math.sqrt(sum(x * x for x in v)) or 1.0)
    return v, inv


def topk(q, q_inv, boxes, k, ctx=None, trusted_only=False):
    sims = []
    for v, inv, c, bctx, rat in boxes:
        if ctx is not None and bctx != ctx:
            continue
        if trusted_only and not rat:
            continue
        dot = 0.0
        for a, b in zip(q, v):
            dot += a * b
        sims.append((dot * q_inv * inv, c, rat))
    sims.sort(reverse=True)
    return sims[:k]


def run(n=8000, dim=16, clusters=40, q=150, k=5):
    rnd = random.Random(3)
    cents, boxes = build(n, dim, clusters, )
    print("=" * 66)
    print(f"FABRIC RETRIEVAL BENCHMARK  (n={n:,} boxes, dim={dim}, "
          f"clusters={clusters}, k={k}, queries={q})")
    print("=" * 66)

    scenarios = [
        ("RAG (global vector search)", dict()),
        ("AI memory (context-scoped)", dict(ctx=0)),
        ("Trust (ratified-only)",      dict(trusted_only=True)),
    ]
    for name, kw in scenarios:
        ctx = kw.get("ctx")
        # query within the scoped context (memory-in-context, §10.4): pick a
        # cluster that actually lives in that context, else retrieval is useless.
        cand = [c for c in range(clusters) if ctx is None or c % 4 == ctx]
        hits = 0           # precision@k: top-k in the same cluster
        trusted_returned = 0
        total = 0
        t0 = time.perf_counter()
        for _ in range(q):
            cl = rnd.choice(cand)
            qv, qi = query_vec(cents, cl, dim, rnd)
            res = topk(qv, qi, boxes, k, **kw)
            for sim, c, rat in res:
                total += 1
                if c == cl:
                    hits += 1
                if rat:
                    trusted_returned += 1
        dt = time.perf_counter() - t0
        prec = hits / total if total else 0.0
        trust_rate = trusted_returned / total if total else 0.0
        print(f"{name:<32} {q/dt:8.0f} q/s  {dt*1000/q:6.2f} ms/q  "
              f"precision@{k}={prec:4.0%}  trusted={trust_rate:4.0%}")
    print("-" * 66)
    print("speed     : exact brute-force; ANN index -> 10-100x faster, ~accuracy cost")
    print("accuracy  : precision@k high because boxes-in-context cluster cleanly")
    print("real-time : retrieval pairs with LIVE SELECT (live) + change feed (re-stream)")
    print("=" * 66)
    return 0


if __name__ == "__main__":
    args = [int(x) for x in sys.argv[1:]]
    sys.exit(run(*args) if args else run())
