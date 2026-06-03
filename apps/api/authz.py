from typing import Set

from .graph import IdentityGraph

ALLOWED_EDGE_TYPES = {"owns", "delegates", "trusts", "member_of"}


def can_act(graph: IdentityGraph, subject: str, target: str, max_depth: int = 4) -> bool:
    """
    Graph-based authorization check.

    Returns True if `subject` can act on `target` based on identity relationships.

    Rules:
    - ownership implies full control
    - delegation implies transitive control
    - trust implies limited propagation
    """

    if subject == target:
        return True

    visited: Set[str] = set()
    queue = [(subject, 0)]

    while queue:
        current, depth = queue.pop(0)

        if depth > max_depth:
            continue

        if current == target:
            return True

        visited.add(current)

        for edge in graph.get_outgoing(current):
            if edge.type not in ALLOWED_EDGE_TYPES:
                continue

            if edge.dst not in visited:
                queue.append((edge.dst, depth + 1))

    return False
