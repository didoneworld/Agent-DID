"""Testcontainer-style backend test for the fabric on SurrealDB.

`test_backend_resolves_on_surrealdb` provisions an ephemeral SurrealDB (Docker
image `surrealdb/surrealdb`, testcontainer style) and asserts the seeded graph
resolves at node + box inside the real backend. It SKIPS cleanly when no Docker /
`surreal` is available, so it never breaks collection.

`test_reference_kernel_resolves` is backend-agnostic: the identical kernel must
resolve in-process, so this always runs and guards the model's logic.
"""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import run_backend  # noqa: E402


def test_backend_resolves_on_surrealdb():
    result = run_backend.run_with_docker() or run_backend.run_with_binary()
    if result is None:
        pytest.skip("no SurrealDB backend (docker image / surreal binary) available")
    assert result["valid"], result
    assert result["node_real"] and result["box_stable"], result


def test_reference_kernel_resolves():
    result = run_backend.run_with_reference()
    assert result["valid"], result
    assert result["node_real"] and result["box_stable"], result
