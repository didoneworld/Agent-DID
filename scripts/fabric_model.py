#!/usr/bin/env python3
"""The model is the graph — a self-describing fabric.

Builds a graph in which the *model itself is part of the graph*: the metamodel
(the kinds, the relations, the schemas) are **boxes** living in the same graph as
the data. Every box is typed by a box; every edge is related by a box; the type
chain terminates in a self-typed fixpoint (`kind` is a `kind`). Validating the
graph therefore validates the model — there is no separate, privileged schema
outside the graph (cf. fabric-of-work.md §7.6.3 "a schema is itself a box",
§7.7 boxes/slots, §10 data is primary).

Resolution mirrors scripts/fabric_graph.py:
  * NODE -> real   : every reference (typing, relation, context, edge) resolves
  * BOX  -> stable : every box is typed, filled, and placed
A self-describing graph is VALID (real + stable) iff its model — being in the
graph — also resolves.
"""
from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass, field


@dataclass
class Box:
    id: str
    kind: str                 # id of a box whose kind == "kind"
    ctx: str | None = None    # id of the context/box it is placed in
    payload: dict = field(default_factory=dict)
    meta: bool = False        # part of the model (metamodel) vs data
    valid_from: float | None = None  # bi-temporal validity (Graphiti/Zep style)
    valid_to: float | None = None    # None = open / always valid

    def valid_at(self, t: float) -> bool:
        return ((self.valid_from is None or self.valid_from <= t)
                and (self.valid_to is None or t < self.valid_to))


class Graph:
    def __init__(self) -> None:
        self.boxes: dict[str, Box] = {}
        self.edges: list[tuple[str, str, str]] = []  # (src, rel_id, dst)
        self._subs: list[tuple] = []  # (predicate, callback) — real-time streams

    def box(self, id, kind, ctx=None, payload=None, meta=False,
            valid_from=None, valid_to=None) -> Box:
        b = Box(id, kind, ctx, payload or {}, meta, valid_from, valid_to)
        self.boxes[id] = b
        self._emit("create", b)
        return b

    def relate(self, src, rel, dst) -> None:
        self.edges.append((src, rel, dst))

    def as_of(self, t: float) -> set:
        """Bi-temporal query: boxes valid at time t (what was believed at t)."""
        return {i for i, b in self.boxes.items() if b.valid_at(t)}

    # ---- real-time box streaming (live query / change feed, §6.1) ----------
    def subscribe(self, predicate, callback) -> None:
        """Register a live consumer; callback(op, box) fires as boxes stream in.
        SurrealDB equivalent: LIVE SELECT * FROM box WHERE <predicate>."""
        self._subs.append((predicate, callback))

    def _emit(self, op: str, b: Box) -> None:
        for predicate, callback in self._subs:
            if predicate(b):
                callback(op, b)

    # ---- JSON-LD: a box is linked data on the wire, a node in the store ----
    def to_jsonld(self, box_id: str) -> dict:
        """Serialize a box to JSON-LD (fabric-of-work.md §3, §10.4): payload
        emitted under its context's @context; edges become predicates."""
        b = self.boxes[box_id]
        doc: dict = {
            "@context": {
                "@vocab": "https://agentdid.dev/fabric#",
                "kind": "@type",
                "ctx": {"@id": "context", "@type": "@id"},
            },
            "@id": f"box:{b.id}",
            "@type": b.kind,
        }
        if b.ctx is not None:
            doc["ctx"] = f"box:{b.ctx}"
        doc.update(b.payload)
        for s, rel, d in self.edges:
            if s == b.id:
                doc.setdefault(rel, []).append(f"box:{d}")
        return doc

    # ---- promotion: digital -> real, gated on resolve + ratify -------------
    def promote(self, box_id: str, ratified: bool) -> Box:
        """Promote a box from digital sandbox to real (§8.4.3). Refused unless
        the whole graph resolves (real + stable) AND the box is ratified (§3.3).
        Failure is explicit (§7.5)."""
        r = self.resolve()
        if not r["valid"]:
            raise ValueError("promotion refused: graph does not resolve "
                             "(not real + stable)")
        if not ratified:
            raise ValueError(f"promotion refused: {box_id} not ratified (§3.3)")
        b = self.boxes[box_id]
        b.payload = {**b.payload, "realm": "real", "state": "stable"}
        self._emit("update", b)
        return b

    # ---- resolution --------------------------------------------------------
    def resolve(self) -> dict:
        B = self.boxes
        dangling: list[str] = []
        # typing edges: every box.kind must be a box whose kind == "kind"
        for b in B.values():
            if b.kind not in B:
                dangling.append(f"type {b.id}->{b.kind} (missing)")
            elif B[b.kind].kind != "kind":
                dangling.append(f"type {b.id}->{b.kind} (not a kind)")
            if b.ctx is not None and b.ctx not in B:
                dangling.append(f"ctx {b.id}->{b.ctx} (missing)")
        # relation edges: src, dst exist; rel is a box whose kind == "relation"
        for s, rel, d in self.edges:
            if s not in B:
                dangling.append(f"edge src {s} (missing)")
            if d not in B:
                dangling.append(f"edge dst {d} (missing)")
            if rel not in B:
                dangling.append(f"edge rel {rel} (missing)")
            elif B[rel].kind != "relation":
                dangling.append(f"edge rel {rel} (not a relation)")

        # box stability: typed + filled + placed
        unstable: list[str] = []
        for b in B.values():
            typed = b.kind in B and B[b.kind].kind == "kind"
            filled = bool(b.payload) or b.kind in ("kind", "relation") or b.meta
            placed = b.ctx in B if b.ctx is not None else (b.id == "kind")
            if not (typed and filled and placed):
                miss = [n for n, ok in (("typed", typed), ("filled", filled),
                                        ("placed", placed)) if not ok]
                unstable.append(f"{b.id} [{','.join(miss)}]")

        # connectivity: every box's type/context chain bottoms out at the
        # self-typed root fixpoint "kind" (reverse traversal: kind -> instances,
        # context -> members, edges undirected for reachability).
        adj: dict[str, set[str]] = {i: set() for i in B}
        for b in B.values():
            if b.kind in B:
                adj[b.kind].add(b.id)   # a kind contains its instances
            if b.ctx in B:
                adj[b.ctx].add(b.id)    # a context contains its members
        for s, rel, d in self.edges:
            if s in B and d in B:
                adj[s].add(d)
                adj[d].add(s)
            if rel in B and s in B:
                adj[rel].add(s)
        seen, q = set(), deque(["kind"])
        while q:
            n = q.popleft()
            if n in seen:
                continue
            seen.add(n)
            q.extend(adj.get(n, ()))
        unreachable = [i for i in B if i not in seen]

        node_real = not dangling
        box_stable = not unstable and not unreachable
        return {
            "dangling": dangling, "unstable": unstable, "unreachable": unreachable,
            "node_real": node_real, "box_stable": box_stable,
            "valid": node_real and box_stable,
        }


def build() -> Graph:
    g = Graph()

    # ---- the metamodel, AS BOXES IN THE GRAPH ----------------------------
    # the fixpoint: a "kind" is a "kind" (self-typed root of the model)
    g.box("kind", kind="kind", ctx=None, meta=True)
    # "relation" is a kind (so edges can be related by boxes)
    g.box("relation", kind="kind", ctx="kind", meta=True)
    # "schema" is a kind (schemas are boxes, §7.6.3)
    g.box("schema", kind="kind", ctx="kind", meta=True)
    # the universal data kind: "box" is a kind
    g.box("box", kind="kind", ctx="kind", meta=True)

    # the domain kinds (§8) — each a box typed by "kind"
    for k in ("context", "command", "tool", "ingredient", "labour",
              "construction", "strategy", "planning", "agent"):
        g.box(k, kind="kind", ctx="kind", meta=True)

    # the relations (§ data model edges) — each a box typed by "relation"
    for r in ("contains", "references", "derives", "fills", "commands",
              "performs", "instance_of"):
        g.box(r, kind="relation", ctx="kind", meta=True)

    # ---- data, in the SAME graph -----------------------------------------
    g.box("ctx:onboarding", kind="context", ctx="kind",
          payload={"name": "onboarding"})
    g.box("agent:alice", kind="agent", ctx="ctx:onboarding",
          payload={"did": "did:example:alice", "value": 1})
    g.box("cmd:provision", kind="command", ctx="ctx:onboarding",
          payload={"action": "provision"})
    g.box("tool:scim", kind="tool", ctx="ctx:onboarding",
          payload={"api": "scim"})
    g.box("ing:box-42", kind="ingredient", ctx="ctx:onboarding",
          payload={"realm": "digital", "value": 42})
    g.box("work:c1", kind="construction", ctx="ctx:onboarding",
          payload={"result": "agent provisioned"})

    # edges (each related by a relation-box -> the model is the graph)
    g.relate("agent:alice", "commands", "cmd:provision")
    g.relate("cmd:provision", "references", "tool:scim")
    g.relate("work:c1", "contains", "ing:box-42")
    g.relate("agent:alice", "performs", "work:c1")
    g.relate("work:c1", "derives", "cmd:provision")
    g.relate("ing:box-42", "fills", "ctx:onboarding")
    return g


def main() -> int:
    g = build()
    r = g.resolve()
    kinds = [b.id for b in g.boxes.values() if b.kind == "kind"]
    rels = [b.id for b in g.boxes.values() if b.kind == "relation"]
    data = [b.id for b in g.boxes.values() if not b.meta]

    print("=" * 66)
    print("THE MODEL IS THE GRAPH — self-describing fabric")
    print("=" * 66)
    print(f"boxes total        : {len(g.boxes)}")
    print(f"  kind-boxes (model): {len(kinds)}  -> {', '.join(kinds)}")
    print(f"  relation-boxes    : {len(rels)}  -> {', '.join(rels)}")
    print(f"  data-boxes        : {len(data)}  -> {', '.join(data)}")
    print(f"edges              : {len(g.edges)}")
    print("-" * 66)
    # the model-is-graph invariants
    every_box_typed_by_box = all(b.kind in g.boxes for b in g.boxes.values())
    every_edge_related_by_box = all(rel in g.boxes and g.boxes[rel].kind == "relation"
                                    for _, rel, _ in g.edges)
    fixpoint = g.boxes["kind"].kind == "kind"
    print(f"every box typed by a box      : {every_box_typed_by_box}")
    print(f"every edge related by a box   : {every_edge_related_by_box}")
    print(f"self-typed fixpoint (kind:kind): {fixpoint}")
    print("-" * 66)
    print(f"[NODE] resolution  : {'REAL' if r['node_real'] else 'UNREAL'} "
          f"({len(r['dangling'])} dangling)")
    for d in r["dangling"]:
        print(f"    DANGLING {d}")
    print(f"[BOX]  resolution  : {'STABLE' if r['box_stable'] else 'UNSTABLE'} "
          f"({len(r['unstable'])} unstable, {len(r['unreachable'])} unreachable)")
    for u in r["unstable"]:
        print(f"    UNSTABLE {u}")
    for u in r["unreachable"]:
        print(f"    UNREACHABLE {u}")
    print("=" * 66)
    ok = r["valid"] and every_box_typed_by_box and every_edge_related_by_box and fixpoint
    print(f"SELF-DESCRIBING GRAPH : {'VALID (real + stable)' if ok else 'INVALID'}")
    print("  the model is in the graph, and the graph (incl. its model) resolves"
          if ok else "  the model/graph does NOT resolve")
    print("=" * 66)

    # ---- JSON-LD: a box is linked data on the wire ----------------------
    print("\nJSON-LD (box:c1 — a construction, linked data on the wire):")
    import json as _json
    print(_json.dumps(g.to_jsonld("work:c1"), indent=2))

    # ---- promotion: digital -> real, gated on resolve + ratify ----------
    print("\nPromotion (digital -> real; batch or real-time, §8.4.3):")
    try:
        g.promote("ing:box-42", ratified=False)
    except ValueError as e:
        print(f"  unratified -> {e}")
    b = g.promote("ing:box-42", ratified=True)
    print(f"  ratified   -> box:ing:box-42 realm={b.payload['realm']} "
          f"state={b.payload['state']}  (now real)")

    # ---- real-time box streaming ----------------------------------------
    print("\nReal-time box streaming (LIVE SELECT, ctx=onboarding, "
          "kind in {command,ingredient}):")
    wanted = {"command", "ingredient"}
    g.subscribe(
        lambda bx: bx.kind in wanted and bx.ctx == "ctx:onboarding",
        lambda op, bx: print(f"  stream <- [{op}] box:{bx.id} "
                             f"kind={bx.kind} payload={bx.payload}"),
    )
    # new work arrives -> consumers receive it live, in order
    g.box("cmd:rotate", kind="command", ctx="ctx:onboarding",
          payload={"action": "rotate-keys"})
    g.box("ing:token", kind="ingredient", ctx="ctx:onboarding",
          payload={"realm": "digital", "value": 7})
    g.box("tool:audit", kind="tool", ctx="ctx:onboarding",
          payload={"api": "audit"})  # filtered out (kind=tool)
    g.promote("ing:token", ratified=True)  # update streams too

    # ---- bi-temporal validity (Graphiti/Zep style: valid_at/invalid_at) --
    print("\nBi-temporal memory (what was true at time T):")
    g.box("fact:budget-owner@alice", kind="ingredient", ctx="ctx:onboarding",
          payload={"owner": "alice"}, valid_from=0, valid_to=10)
    g.box("fact:budget-owner@bob", kind="ingredient", ctx="ctx:onboarding",
          payload={"owner": "bob"}, valid_from=10)
    for t in (5, 15):
        owners = [g.boxes[i].payload["owner"]
                  for i in g.as_of(t) if i.startswith("fact:budget-owner")]
        print(f"  as_of t={t:<3} budget owner -> {owners}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
