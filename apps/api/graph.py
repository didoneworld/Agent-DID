from typing import Dict, List, Optional
from dataclasses import dataclass, field
import uuid


@dataclass
class Node:
    id: str
    type: str  # agent | user | org | service
    data: dict = field(default_factory=dict)


@dataclass
class Edge:
    id: str
    src: str
    dst: str
    type: str  # owns | delegates | trusts | member_of
    meta: dict = field(default_factory=dict)


class IdentityGraph:
    """
    In-memory graph database for Agent DID.
    No docker, no external DB required.
    This is the vendor-neutral graph core.
    """

    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}

    # -------------------- Nodes --------------------

    def add_node(self, node_type: str, data: dict) -> Node:
        node_id = str(uuid.uuid4())
        node = Node(id=node_id, type=node_type, data=data)
        self.nodes[node_id] = node
        return node

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def list_nodes(self, node_type: Optional[str] = None) -> List[Node]:
        if node_type:
            return [n for n in self.nodes.values() if n.type == node_type]
        return list(self.nodes.values())

    # -------------------- Edges --------------------

    def add_edge(self, src: str, dst: str, edge_type: str, meta: dict = None) -> Edge:
        if src not in self.nodes or dst not in self.nodes:
            raise ValueError("Invalid node reference")

        edge_id = str(uuid.uuid4())
        edge = Edge(
            id=edge_id,
            src=src,
            dst=dst,
            type=edge_type,
            meta=meta or {}
        )
        self.edges[edge_id] = edge
        return edge

    def get_edges(self, node_id: str) -> List[Edge]:
        return [e for e in self.edges.values() if e.src == node_id or e.dst == node_id]

    def get_outgoing(self, node_id: str) -> List[Edge]:
        return [e for e in self.edges.values() if e.src == node_id]

    def get_incoming(self, node_id: str) -> List[Edge]:
        return [e for e in self.edges.values() if e.dst == node_id]

    # -------------------- Queries --------------------

    def find_path(self, start: str, end: str, max_depth: int = 3) -> List[str]:
        """Simple BFS path finder (limited depth)"""
        from collections import deque

        queue = deque([(start, [start])])
        visited = set()

        while queue:
            current, path = queue.popleft()

            if current == end:
                return path

            if len(path) > max_depth:
                continue

            visited.add(current)

            for edge in self.get_outgoing(current):
                if edge.dst not in visited:
                    queue.append((edge.dst, path + [edge.dst]))

        return []
