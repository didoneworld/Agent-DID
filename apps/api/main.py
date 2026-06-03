from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import uuid

app = FastAPI(title="Agent DID Control Plane")

# --- In-memory demo stores (replace with Postgres later) ---
AGENT_REGISTRY: Dict[str, dict] = {}
API_KEYS: Dict[str, str] = {}


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


@app.get("/health")
def health():
    return {"status": "ok", "service": "agent-did"}


@app.post("/v1/bootstrap")
def bootstrap(req: BootstrapRequest):
    api_key = str(uuid.uuid4())
    API_KEYS[api_key] = req.organization_slug

    return {
        "organization": req.organization_slug,
        "api_key": api_key,
        "message": "tenant bootstrapped"
    }


@app.post("/v1/agent-records")
def create_agent(record: AgentRecord, x_api_key: str = Header(None)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    AGENT_REGISTRY[record.agent_id] = record.model_dump()

    return {"status": "created", "agent": record.model_dump()}


@app.get("/v1/agent-records")
def list_agents(x_api_key: str = Header(None)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {"agents": list(AGENT_REGISTRY.values())}
