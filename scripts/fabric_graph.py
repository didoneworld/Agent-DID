#!/usr/bin/env python3
"""Fabric graph resolver.

Constructs the Fabric of Work constitution (docs/fabric-of-work.md) as a graph
and validates it against its own criteria:

  * NODE resolution  - every "§" reference resolves to a defined section/clause
                       node (the graph; cf. §9 graph/DAG mode).
  * BOX  resolution  - each node, transformed into a *box* (§7.7), is:
                         - filled    : has content, never structureless (§7.6.4)
                         - placed    : sits in a valid context-slot/parent (§1, §7.7)
                         - resolving : all of its outgoing references resolve
                       and the whole is connected (every box reachable from root).

The system is VALID (real) iff it resolves at node AND box (§ "the graph must
resolve at node and box for the system to be valid, or real"). Exits non-zero on
failure so the check is explicit (§7.5).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOC = Path(__file__).resolve().parent.parent / "docs" / "fabric-of-work.md"
EXTERNAL_DOC = Path(__file__).resolve().parent.parent / "docs" / "design-principles.md"

HEADER_RE = re.compile(r"^#{1,3}\s+(\d+(?:\.\d+)*)\.\s+(.*)$")
ROOT_RE = re.compile(r"^#\s+The Fabric")
CLAUSE_RE = re.compile(r"^(\d+(?:\.\d+)+)\.\s+\S")
REF_RE = re.compile(r"§\s*(\d+(?:\.\d+)*)")
EXT_HEADER_RE = re.compile(r"^#\s+(\d+)\.\s")


def parent_of(node_id: str, nodes: dict) -> str:
    """Walk up the dotted id until an existing node (the context-slot) is found."""
    parts = node_id.split(".")
    while len(parts) > 1:
        parts = parts[:-1]
        candidate = ".".join(parts)
        if candidate in nodes:
            return candidate
    return "root"


def load_external_sections() -> set[str]:
    if not EXTERNAL_DOC.exists():
        return set()
    ids = set()
    for line in EXTERNAL_DOC.read_text(encoding="utf-8").splitlines():
        m = EXT_HEADER_RE.match(line)
        if m:
            ids.add(m.group(1))
    return ids


def build() -> int:
    text = DOC.read_text(encoding="utf-8")
    lines = text.splitlines()

    # ---- nodes -----------------------------------------------------------
    nodes: dict[str, dict] = {"root": {"title": "The Fabric of Work", "content": 0}}
    order: list[str] = ["root"]
    current: str = "root"
    for ln in lines:
        nid = None
        title = ""
        inline = ""
        if HEADER_RE.match(ln):
            hm = HEADER_RE.match(ln)
            nid, title = hm.group(1), hm.group(2)
            inline = title  # a section is named by its header
        elif CLAUSE_RE.match(ln):
            cm = re.match(r"^(\d+(?:\.\d+)+)\.\s+(.*)$", ln)
            nid = cm.group(1)
            inline = cm.group(2)  # a one-line clause carries content on its own line
            title = inline[:60]
        if nid:
            if nid not in nodes:
                nodes[nid] = {"title": title, "content": len(inline.strip())}
                order.append(nid)
            current = nid
        elif ln.strip():
            nodes[current]["content"] += len(ln.strip())
    if ROOT_RE.search(text):
        nodes["root"]["content"] += 1

    # parents (context-slots) and children (contained boxes)
    for nid in nodes:
        nodes[nid]["parent"] = "root" if nid == "root" else parent_of(nid, nodes)
    children: dict[str, int] = {nid: 0 for nid in nodes}
    for nid in nodes:
        if nid != "root":
            children[nodes[nid]["parent"]] += 1

    # ---- references / edges ---------------------------------------------
    external_ids = load_external_sections()
    edges: list[tuple[str, str, bool]] = []  # (src, ref_id, external)
    current = "root"
    for ln in lines:
        if HEADER_RE.match(ln):
            current = HEADER_RE.match(ln).group(1)
        elif CLAUSE_RE.match(ln):
            current = CLAUSE_RE.match(ln).group(1)
        for m in REF_RE.finditer(ln):
            before = ln[max(0, m.start() - 30):m.start()]
            external = "design-principles" in before
            edges.append((current, m.group(1), external))

    # ---- NODE resolution -------------------------------------------------
    dangling = []
    for src, ref, external in edges:
        if external:
            if ref not in external_ids:
                dangling.append((src, f"§{ref}", "external/design-principles.md"))
        else:
            if ref not in nodes:
                dangling.append((src, f"§{ref}", "internal"))

    # ---- BOX transform + resolution -------------------------------------
    # adjacency for connectivity = containment (parent->child) ∪ internal refs
    adj: dict[str, set[str]] = {nid: set() for nid in nodes}
    indeg_ref: dict[str, int] = {nid: 0 for nid in nodes}
    outdeg_ref: dict[str, int] = {nid: 0 for nid in nodes}
    for nid in nodes:
        p = nodes[nid]["parent"]
        if nid != "root":
            adj[p].add(nid)
    for src, ref, external in edges:
        if not external and ref in nodes:
            adj.setdefault(src, set()).add(ref)
            outdeg_ref[src] = outdeg_ref.get(src, 0) + 1
            indeg_ref[ref] = indeg_ref.get(ref, 0) + 1

    boxes = {}
    unresolved_boxes = []
    for nid in nodes:
        # filled: carries own content OR contains boxes (a slot filled by boxes, §7.7)
        filled = nodes[nid]["content"] > 0 or children[nid] > 0
        placed = nid == "root" or nodes[nid]["parent"] in nodes
        refs_ok = all(
            (ref in external_ids) if external else (ref in nodes)
            for s, ref, external in edges
            if s == nid
        )
        resolves = filled and placed and refs_ok
        boxes[nid] = {"filled": filled, "placed": placed, "refs_ok": refs_ok, "resolves": resolves}
        if not resolves:
            unresolved_boxes.append((nid, boxes[nid]))

    # connectivity: every box reachable from root via containment ∪ refs
    seen = set()
    stack = ["root"]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(adj.get(n, ()))
    unreachable = [nid for nid in nodes if nid not in seen]

    orphans = [
        nid for nid in nodes
        if nid != "root" and indeg_ref[nid] == 0 and outdeg_ref[nid] == 0
    ]

    # ---- report ----------------------------------------------------------
    node_ok = not dangling
    box_ok = not unresolved_boxes and not unreachable
    valid = node_ok and box_ok

    print("=" * 64)
    print("FABRIC GRAPH RESOLVER  —  docs/fabric-of-work.md")
    print("=" * 64)
    print(f"nodes (boxes)        : {len(nodes)}")
    print(f"references (edges)   : {len(edges)}  "
          f"({sum(1 for *_, e in edges if e)} external)")
    print(f"containment slots    : {sum(len(v) for v in adj.values())} edges total")
    print("-" * 64)
    print(f"[NODE] resolution    : {'REAL' if node_ok else 'UNREAL'} "
          f"({len(dangling)} dangling references)")
    for src, ref, kind in dangling:
        print(f"    DANGLING  §ref {ref} in node {src}  [{kind}]")
    print(f"[BOX]  resolution    : {'STABLE' if box_ok else 'UNSTABLE'} "
          f"({len(unresolved_boxes)} unresolved, {len(unreachable)} unreachable)")
    for nid, b in unresolved_boxes:
        why = [k for k in ("filled", "placed", "refs_ok") if not b[k]]
        print(f"    UNRESOLVED box {nid}  failing: {', '.join(why)}")
    for nid in unreachable:
        print(f"    UNREACHABLE box {nid}")
    print("-" * 64)
    print(f"orphan boxes (no ref in/out, still contained): {len(orphans)}")
    if orphans:
        print("    " + ", ".join(orphans))
    print("=" * 64)
    print("semantics: node -> real   box -> stable   graph -> real")
    print(f"SYSTEM VALIDITY      : {'VALID (real + stable)' if valid else 'INVALID (not real)'}")
    print("  the graph resolves at node (real) AND box (stable)"
          if valid else "  the graph does NOT resolve at node and box")
    print("=" * 64)
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(build())
