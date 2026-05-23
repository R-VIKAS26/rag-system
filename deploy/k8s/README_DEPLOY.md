Kubernetes Deployment Guide
==========================

This folder contains minimal Kubernetes manifests for deploying the `ragsystem` backend and frontend.

Prerequisites:
- A container registry (Docker Hub, GCR, ECR, etc.)
- `kubectl` configured to your cluster
- Optional: an ingress controller for external access

Steps:

1. Build and tag images locally (example using Docker):

```bash
docker build -t your-registry/ragsystem-backend:latest -f backend/Dockerfile .
docker build -t your-registry/ragsystem-frontend:latest -f frontend/Dockerfile.dev .
docker push your-registry/ragsystem-backend:latest
docker push your-registry/ragsystem-frontend:latest
```

2. Create Kubernetes secrets for API keys (example):

```bash
kubectl create secret generic ragsystem-secrets --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" --from-literal=ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
```

3. Update the image references in the YAML files above to point to your registry (or use `kubectl set image`).

4. Apply manifests:

```bash
kubectl apply -f deploy/k8s/backend-deployment.yaml
kubectl apply -f deploy/k8s/frontend-deployment.yaml
```

5. Expose services via an Ingress or `kubectl port-forward` for quick testing.

Notes:
- These manifests are intentionally minimal. For production, add resource limits, probes, RBAC, namespace isolation, and storage for Postgres/Chroma.
- Consider using Helm for templating and easier upgrades.
