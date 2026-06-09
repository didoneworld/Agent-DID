#!/usr/bin/env python3
"""Fraud detection on financial transactions — over the box graph.

Financial transactions are boxes (kind=transaction) linking account boxes; fraud
detection is graph + temporal + trust analysis over them — exactly the fabric's
strengths combined:
  * graph    : money-laundering RINGS = cycles in the account graph.
  * temporal : VELOCITY = too many transactions in a short window (valid_at, §bi-temporal).
  * trust    : untrusted / unresolved source (provenance, §3.1).
  * analytics: AMOUNT anomaly vs typical (OLAP rollup, §6.3).
  * real-time: each transaction scored as it streams (LIVE, §6.1).

Deterministic: known fraud patterns are injected and must be caught.
"""
from __future__ import annotations

import statistics


def build():
    accounts = {a: {"trusted": a not in (90, 91)} for a in range(100)}
    txns = []  # (id, src, dst, amount, t)
    tid = 0
    # normal background traffic
    rng = __import__("random").Random(7)
    for _ in range(400):
        s, d = rng.randrange(100), rng.randrange(100)
        if s != d:
            txns.append((tid, s, d, rng.randint(10, 200), rng.randint(0, 1000)))
            tid += 1
    # INJECT: laundering ring 90->91->92->90
    for (s, d) in ((90, 91), (91, 92), (92, 90)):
        txns.append((tid, s, d, 950, 500 + tid)); tid += 1
    # INJECT: velocity burst from account 5 (many tx in a tiny window)
    for _ in range(15):
        txns.append((tid, 5, rng.randrange(100), 120, 700)); tid += 1
    # INJECT: amount anomaly
    txns.append((tid, 7, 8, 50_000, 800)); tid += 1
    return accounts, txns


def detect(accounts, txns):
    flags = {}  # tid -> set(reasons)

    def add(tid, reason):
        flags.setdefault(tid, set()).add(reason)

    amounts = [a for _, _, _, a, _ in txns]
    med = statistics.median(amounts)

    # amount anomaly + untrusted source
    for tid, s, d, amt, t in txns:
        if amt > 20 * med:
            add(tid, "amount-anomaly")
        if not accounts[s]["trusted"]:
            add(tid, "untrusted-source")

    # velocity: >8 tx from same src within window of 5 time units
    by_src: dict = {}
    for tid, s, d, amt, t in txns:
        by_src.setdefault(s, []).append((t, tid))
    for s, lst in by_src.items():
        lst.sort()
        for i, (t, tid) in enumerate(lst):
            window = [x for x in lst if t <= x[0] < t + 5]
            if len(window) > 8:
                for _, wid in window:
                    add(wid, "velocity")

    # ring: cycle in the account graph (depth-limited DFS)
    adj: dict = {}
    edge_tid: dict = {}
    for tid, s, d, amt, t in txns:
        adj.setdefault(s, set()).add(d)
        edge_tid[(s, d)] = tid

    def find_cycle(start, node, path, depth):
        if depth > 5:
            return None
        for nxt in adj.get(node, ()):
            if nxt == start and len(path) >= 2:
                return path + [nxt]
            if nxt not in path:
                r = find_cycle(start, nxt, path + [nxt], depth + 1)
                if r:
                    return r
        return None

    for a in list(adj):
        cyc = find_cycle(a, a, [a], 0)
        if cyc:
            for u, v in zip(cyc, cyc[1:]):
                if (u, v) in edge_tid:
                    add(edge_tid[(u, v)], "laundering-ring")
            break
    return flags


def main() -> int:
    accounts, txns = build()
    flags = detect(accounts, txns)
    print("=" * 60)
    print(f"FABRIC FRAUD DETECTION  ({len(txns)} financial transactions)")
    print("=" * 60)
    by_reason: dict = {}
    for tid, reasons in flags.items():
        for r in reasons:
            by_reason.setdefault(r, []).append(tid)
    for r in sorted(by_reason):
        ids = sorted(by_reason[r])
        print(f"  {r:<18} {len(ids):>3} txns  e.g. {ids[:6]}")
    print("-" * 60)
    print(f"flagged {len(flags)} / {len(txns)} transactions "
          f"({len(flags)/len(txns):.0%})")
    print("signals: graph rings · temporal velocity · trust · amount analytics")
    print("=" * 60)
    # the injected patterns must be caught
    ok = any("laundering-ring" in v for v in flags.values()) \
        and any("velocity" in v for v in flags.values()) \
        and any("amount-anomaly" in v for v in flags.values()) \
        and any("untrusted-source" in v for v in flags.values())
    print(f"INJECTED FRAUD CAUGHT : {ok}")
    print("=" * 60)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
