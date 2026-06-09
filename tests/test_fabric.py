"""Test suite for the Fabric of Work artifacts.

Each fabric script self-validates and exits non-zero on failure (failure is
explicit, fabric-of-work.md §7.5). These tests run each as a subprocess and
assert exit 0 plus a result marker, so the whole bundle is verified end to end
without importing internals. Runnable with `pytest tests/test_fabric.py`.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(script, *args):
    r = subprocess.run([sys.executable, str(ROOT / script), *args],
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, f"{script} exited {r.returncode}\n{r.stdout}\n{r.stderr}"
    return r.stdout


def test_constitution_resolves():
    assert "VALID (real + stable)" in run("scripts/fabric_graph.py")


def test_self_describing_model_resolves():
    out = run("scripts/fabric_model.py")
    assert "SELF-DESCRIBING GRAPH : VALID" in out
    assert "as_of t=5" in out and "as_of t=15" in out  # bi-temporal


def test_enterprise_models_resolve():
    assert "ALL VALID (real + stable)" in run("scripts/fabric_enterprise.py")


def test_scale_resolves():
    out = run("scripts/fabric_scale_bench.py", "10000", "50000")
    assert "node=real" in out and "box=stable" in out


def test_retrieval_precision():
    out = run("scripts/fabric_rag_bench.py")
    assert "precision@5" in out


def test_agent_scorecard():
    out = run("scripts/fabric_agent_score.py")
    assert "GPA" in out and "RISK & THREAT PROFILE" in out


def test_chaos_resilience():
    out = run("scripts/fabric_chaos.py", "10000", "5")
    assert "chaos score" in out and "blast radius" in out


def test_fraud_detection_catches_injected():
    assert "INJECTED FRAUD CAUGHT : True" in run("scripts/fabric_fraud.py")


def test_htap_oltp_and_olap():
    out = run("scripts/fabric_htap.py", "20000")
    assert "[OLTP]" in out and "[OLAP]" in out


def test_backend_resolves():
    assert "VALID (real + stable)" in run("experiments/fabric/run_backend.py")
