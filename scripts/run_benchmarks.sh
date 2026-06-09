#!/usr/bin/env bash
# Reproduce all fabric benchmarks in one command (public, deterministic, offline).
# Usage:  bash scripts/run_benchmarks.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "########## 1. constitution resolves (node + box) ##########"
python3 scripts/fabric_graph.py

echo; echo "########## 2. self-describing stable-state model ##########"
python3 scripts/fabric_model.py | tail -n 6

echo; echo "########## 3. resolution scale (-> 8e9 federated) ##########"
python3 scripts/fabric_scale_bench.py 100000 1000000

echo; echo "########## 4. retrieval: RAG / AI memory / trust ##########"
python3 scripts/fabric_rag_bench.py

echo; echo "########## 5. agent scorecard: GPA + risk ##########"
python3 scripts/fabric_agent_score.py

echo; echo "########## 6. chaos / resilience score ##########"
python3 scripts/fabric_chaos.py

echo; echo "########## 7. backend resolution (SurrealDB or reference) ##########"
python3 experiments/fabric/run_backend.py

echo; echo "ALL BENCHMARKS COMPLETE — see docs/BENCHMARKS.md"
