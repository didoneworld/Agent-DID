from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import uuid

from .graph import IdentityGraph
from .authz import can_act

app = FastAPI(title="Agent DID Control Plane")

# --- In-memory demo stores (replace with Postgres later) ---
AGENT_REGISTRY: Dict[str, dict] = {}
API_KEYS: Dict[str, str] = {}
API_KEY_NODES: Dict[str, str] = {}

# --- Identity Graph (core system) ---
graph = IdentityGraph()


class BootstrapRequest(BaseModel):
    organization_name: str
    organization_slug: str
    api_key_label: Optional[str] = "default"


class AgentRecord(BaseModel):
    agent_id: str
    did: str
    name: str
    capabilities: list[str] = []
    environment: Optional[str] = "dev"


class GraphNodeRequest(BaseModel):
    type: str
    data: dict = {}


class GraphEdgeRequest(BaseModel):
    src: str
    dst: str
    type: str
    meta: dict = {}


@app.get("/health")
def health():
    return {"status": "ok", "service": "agent-did"}


@app.post("/v1/bootstrap")
def bootstrap(req: BootstrapRequest):
    api_key = str(uuid.uuid4())
    API_KEYS[api_key] = req.organization_slug

    # create identity node for API key subject
    node = graph.add_node(
        node_type="subject",
        data={"api_key": api_key, "org": req.organization_slug}
    )
    API_KEY_NODES[api_key] = node.id

    return {
        "organization": req.organization_slug,
        "api_key": api_key,
        "message": "tenant bootstrapped"
    }


def require_auth(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@app.post("/v1/agent-records")
def create_agent(record: AgentRecord, x_api_key: str = Header(None)):
    api_key = require_auth(x_api_key)

    subject = API_KEY_NODES[api_key]

    if not can_act(graph, subject, "graph"):
        raise HTTPException(status_code=403, detail="Not authorized")

    AGENT_REGISTRY[record.agent_id] = record.model_dump()

    node = graph.add_node(
        node_type="agent",
        data=record.model_dump()
    )

    return {"status": "created", "agent": record.model_dump(), "node_id": node.id}


@app.get("/v1/agent-records")
def list_agents(x_api_key: str = Header(None)):
    api_key = require_auth(x_api_key)
    subject = API_KEY_NODES[api_key]

    if not can_act(graph, subject, "graph"):
        raise HTTPException(status_code=403, detail="Not authorized")

    return {"agents": list(AGENT_REGISTRY.values())}


# ---------------- GRAPH API ----------------

@app.post("/v1/graph/node")
def create_node(req: GraphNodeRequest, x_api_key: str = Header(None)):
    api_key = require_auth(x_api_key)
    subject = API_KEY_NODES[api_key]

    if not can_act(graph, subject, "graph"):
        raise HTTPException(status_code=403, detail="Not authorized")

    node = graph.add_node(req.type, req.data)
    return {"node_id": node.id, "type": node.type}


@app.get("/v1/graph/nodes")
def list_nodes(x_api_key: str = Header(None)):
    api_key = require_auth(x_api_key)
    subject = API_KEY_NODES[api_key]

    if not can_act(graph, subject, "graph"):
        raise HTTPException(status_code=403, detail="Not authorized")

    return {"nodes": [n.__dict__ for n in graph.list_nodes()]}


@app.post("/v1/graph/edge")
def create_edge(req: GraphEdgeRequest, x_api_key: str = Header(None)):
    api_key = require_auth(x_api_key)
    subject = API_KEY_NODES[api_key]

    if not can_act(graph, subject, "graph"):
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        edge = graph.add_edge(req.src, req.dst, req.type, req.meta)
        return {"edge_id": edge.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/v1/graph/path")
def find_path(start: str, end: str, x_api_key: str = Header(None)):
    api_key = require_auth(x_api_key)
    subject = API_KEY_NODES[api_key]

    if not can_act(graph, subject, "graph"):
        raise HTTPException(status_code=403, detail="Not authorized")

    path = graph.find_path(start, end)
    return {"path": path}