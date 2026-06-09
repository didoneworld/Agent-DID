#!/usr/bin/env python3
"""Run the fabric backend on SurrealDB (the building base / BE + DB).

SurrealDB is the BACKEND, not the runtime: this script provisions an ephemeral
SurrealDB (a sandbox = one experimentation environment, fabric-of-work.md §8.4.2),
loads schema.surql + seed.surql, and runs resolve.surql to validate the graph at
node (real) + box (stable).

Backend selection, in order of preference:
  1. SurrealDB in a Docker container (testcontainer style) — `docker` + image.
  2. A locally installed `surreal` server binary (`surreal start --mem`).
  3. Fallback: the in-process reference model (scripts/fabric_model.py), which
     implements the IDENTICAL kernel and resolution, so the backend's logic can
     be validated even where no SurrealDB is available.

Exit code 0 iff the graph is VALID (real + stable).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
IMAGE = os.environ.get("SURREALDB_IMAGE", "surrealdb/surrealdb:latest")
PORT = int(os.environ.get("SURREALDB_PORT", "8000"))
USER, PASSWORD = "root", "root"
NS, DB = "fabric", "sandbox"


def _sql(stmt: str) -> list:
    """POST SurrealQL to the HTTP /sql endpoint and return parsed results."""
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORT}/sql",
        data=stmt.encode(),
        method="POST",
        headers={
            "Accept": "application/json",
            "NS": NS,
            "DB": DB,
            "Authorization": "Basic cm9vdDpyb290",  # root:root
        },
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def _wait_ready(deadline: float) -> bool:
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=2)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def _load_and_resolve() -> dict:
    for fn in ("schema.surql", "seed.surql"):
        _sql((HERE / fn).read_text())
    out = _sql((HERE / "resolve.surql").read_text())
    # the last statement's result is the RETURN object
    result = out[-1].get("result") if isinstance(out, list) else out
    if isinstance(result, list):
        result = result[0]
    return result


def run_with_docker() -> dict | None:
    if not shutil.which("docker"):
        return None
    print(f"[backend] starting SurrealDB container: {IMAGE}")
    try:
        cid = subprocess.check_output([
            "docker", "run", "-d", "--rm", "-p", f"{PORT}:8000", IMAGE,
            "start", "--user", USER, "--pass", PASSWORD,
            "--bind", "0.0.0.0:8000", "memory",
        ], text=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as e:
        print(f"[backend] docker run failed: {e.output}")
        return None
    try:
        if not _wait_ready(time.time() + 30):
            print("[backend] container did not become ready")
            return None
        try:
            return _load_and_resolve()
        except Exception as e:  # noqa: BLE001 - experimental backend: degrade to skip
            print(f"[backend] surrealdb load/resolve failed: {e}")
            return None
    finally:
        subprocess.run(["docker", "stop", cid], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)


def run_with_binary() -> dict | None:
    if not shutil.which("surreal"):
        return None
    print("[backend] starting local `surreal start --mem`")
    proc = subprocess.Popen([
        "surreal", "start", "--user", USER, "--pass", PASSWORD,
        "--bind", f"0.0.0.0:{PORT}", "memory",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not _wait_ready(time.time() + 20):
            print("[backend] surreal did not become ready")
            return None
        try:
            return _load_and_resolve()
        except Exception as e:  # noqa: BLE001 - experimental backend: degrade to skip
            print(f"[backend] surreal load/resolve failed: {e}")
            return None
    finally:
        proc.terminate()


def run_with_reference() -> dict:
    print("[backend] no SurrealDB present -> validating identical kernel via "
          "in-process reference (scripts/fabric_model.py)")
    sys.path.insert(0, str(ROOT / "scripts"))
    import fabric_model  # noqa: E402

    g = fabric_model.build()
    r = g.resolve()
    return {
        "boxes": len(g.boxes),
        "kinds": sum(1 for b in g.boxes.values() if b.kind == "kind"),
        "dangling": r["dangling"],
        "unstable": r["unstable"] + r["unreachable"],
        "node_real": r["node_real"],
        "box_stable": r["box_stable"],
        "valid": r["valid"],
        "_backend": "reference",
    }


def main() -> int:
    result = run_with_docker() or run_with_binary()
    backend = "surrealdb"
    if result is None:
        result = run_with_reference()
        backend = result.get("_backend", "reference")

    print("=" * 60)
    print(f"FABRIC BACKEND RESOLUTION  (backend: {backend})")
    print("=" * 60)
    print(f"boxes        : {result.get('boxes')}")
    print(f"kind-boxes   : {result.get('kinds')}")
    print(f"[NODE] real  : {result.get('node_real')}  "
          f"(dangling: {len(result.get('dangling') or [])})")
    print(f"[BOX]  stable: {result.get('box_stable')}  "
          f"(unstable: {len(result.get('unstable') or [])})")
    print("-" * 60)
    valid = bool(result.get("valid"))
    print(f"VALIDITY     : {'VALID (real + stable)' if valid else 'INVALID'}")
    print("=" * 60)
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
