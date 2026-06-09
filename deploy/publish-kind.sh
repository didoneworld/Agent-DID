#!/usr/bin/env bash
# Publish the Enterprise Agent OS to a local Kubernetes (KinD) cluster.
# Requires: docker, kind, kubectl.
set -euo pipefail
cd "$(dirname "$0")/.."

CLUSTER="${CLUSTER:-agent-os}"
IMAGE="${IMAGE:-agent-identity:local}"

echo "==> 1/5 build app image ($IMAGE) from the repo Dockerfile"
docker build -t "$IMAGE" .

echo "==> 2/5 create KinD cluster ($CLUSTER) with ingress port mappings"
if ! kind get clusters | grep -qx "$CLUSTER"; then
  kind create cluster --name "$CLUSTER" --config deploy/kind/cluster.yaml
fi

echo "==> 3/5 install ingress-nginx"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl -n ingress-nginx wait --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller --timeout=180s

echo "==> 4/5 load app image into the cluster"
kind load docker-image "$IMAGE" --name "$CLUSTER"

echo "==> 5/5 deploy manifests"
kubectl apply -k deploy/k8s
kubectl -n agent-os rollout status deploy/postgres --timeout=180s
kubectl -n agent-os rollout status deploy/agent-os --timeout=180s

cat <<'EOF'

Published. To reach it:
  echo "127.0.0.1 agent-os.local" | sudo tee -a /etc/hosts
  curl http://agent-os.local/health
Tear down:
  kind delete cluster --name agent-os
EOF
