# Publishing the Enterprise Agent OS on Kubernetes (KinD)

Deploys the Agent DID control plane (the Enterprise Agent OS runtime) on a local
**KinD** (Kubernetes IN Docker) cluster, with Postgres and an ingress.

## One command

```bash
bash deploy/publish-kind.sh
```

This builds the app image from the repo `Dockerfile`, creates a KinD cluster
(`deploy/kind/cluster.yaml`), installs ingress-nginx, loads the image, and applies
the manifests (`deploy/k8s/`). Then:

```bash
echo "127.0.0.1 agent-os.local" | sudo tee -a /etc/hosts
curl http://agent-os.local/health
```

## Manifests (`deploy/k8s/`, kustomize)

| File | Resource |
|---|---|
| `namespace.yaml` | `agent-os` namespace |
| `secret.yaml` | `SESSION_SIGNING_SECRET`, DB URL/password (**change for prod**) |
| `postgres.yaml` | Postgres 16 Deployment + Service + PVC |
| `app.yaml` | app Deployment (2 replicas, `/health` probes) + Service |
| `ingress.yaml` | nginx Ingress on `agent-os.local` |
| `kustomization.yaml` | ties them together (`kubectl apply -k deploy/k8s`) |

## Apply to any cluster

```bash
kubectl apply -k deploy/k8s          # any Kubernetes (EKS/GKE/AKS/on-prem)
```

For production: replace the `Secret`, build/push the image to a registry and set
`image:` in `app.yaml`, scale `replicas`, and use a managed Postgres
(`DATABASE_URL`) or a SurrealDB backend per the substrate design.

## Requirements

`docker`, [`kind`](https://kind.sigs.k8s.io/), `kubectl`. (The build dir and the
cluster run on your host; this repo ships the manifests and the script.)
