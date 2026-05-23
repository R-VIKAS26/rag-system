RAG System Helm Chart
---------------------

This Helm chart installs the backend and frontend, with optional Postgres PVC and an optional secret.

Quick install (recommended to create secrets manually):

```bash
# build and push images, then:
helm install ragsystem deploy/helm/ragsystem --set image.backend.repository=your-registry/ragsystem-backend --set image.frontend.repository=your-registry/ragsystem-frontend
```

To create OpenAI secret manually (preferred):

```bash
kubectl create secret generic ragsystem-openai --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY"
helm install ragsystem deploy/helm/ragsystem
```

To enable ingress, set `ingress.enabled=true` and configure `ingress.hostname`.
