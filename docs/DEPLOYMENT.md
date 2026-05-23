# Deployment Guide

## 🚀 Deployment Overview

This guide covers deployment of the Enterprise RAG System across different environments.

## 📋 Prerequisites

- Docker & Docker Compose
- Kubernetes cluster (for K8s deployment)
- PostgreSQL database
- Redis cache
- Chroma DB instance
- Valid API keys (OpenAI, Anthropic, etc.)

## 🐳 Docker Compose Deployment

### Development Environment

```bash
# Clone repository
git clone <repo-url>
cd RAG\ SYSTEM

# Start all services
docker-compose up -d

# Verify services
docker-compose ps

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Configuration

Edit `.env` file before running:

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# Update docker-compose.yml as needed
```

### Service Endpoints

| Service | URL |
|---------|-----|
| Frontend | http://localhost:4200 |
| Backend | http://localhost:8000 |
| API Docs | http://localhost:8000/api/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Chroma | http://localhost:8001 |

## ☸️ Kubernetes Deployment

### 1. Prepare Cluster

```bash
# Create namespace
kubectl create namespace rag-system

# Create secrets
kubectl create secret generic rag-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=redis-url=$REDIS_URL \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  -n rag-system

# Verify secrets
kubectl get secrets -n rag-system
```

### 2. Deploy Infrastructure

```bash
# Create ConfigMap and core resources
kubectl apply -f infrastructure/k8s-config.yaml

# Verify
kubectl get configmap,secrets -n rag-system
```

### 3. Deploy Backend

```bash
# Deploy backend
kubectl apply -f infrastructure/k8s-backend.yaml

# Check deployment
kubectl rollout status deployment/rag-backend -n rag-system

# View pods
kubectl get pods -n rag-system

# View services
kubectl get svc -n rag-system
```

### 4. Scale Deployment

```bash
# Scale backend replicas
kubectl scale deployment rag-backend --replicas=5 -n rag-system

# View autoscaling
kubectl get hpa -n rag-system
```

### 5. Monitor Deployment

```bash
# Stream logs
kubectl logs -f deployment/rag-backend -n rag-system

# Describe pod
kubectl describe pod <pod-name> -n rag-system

# Port forward for local access
kubectl port-forward service/rag-backend-service 8000:80 -n rag-system
```

## ☁️ Cloud Deployment

### AWS ECS

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name rag-system

# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Run service
aws ecs create-service \
  --cluster rag-system \
  --service-name rag-backend \
  --task-definition rag-backend:1 \
  --desired-count 3
```

### Google Cloud Run

```bash
# Deploy backend
gcloud run deploy rag-backend \
  --source . \
  --region us-central1 \
  --platform managed

# Deploy frontend
gcloud run deploy rag-frontend \
  --source frontend \
  --region us-central1 \
  --platform managed
```

### Azure Container Instances

```bash
# Create container group
az container create \
  --resource-group rag-system \
  --name rag-backend \
  --image rag-backend:latest \
  --environment-variables \
    DATABASE_URL=$DATABASE_URL \
    REDIS_URL=$REDIS_URL
```

## 📊 Production Setup Checklist

### Application Configuration
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure production `DATABASE_URL`
- [ ] Set `CORS_ORIGINS` to actual domain
- [ ] Configure logging level to INFO
- [ ] Enable `PROMETHEUS_ENABLED`
- [ ] Configure `SENTRY_DSN` (error tracking)

### Security
- [ ] HTTPS/TLS certificates configured
- [ ] API rate limiting enabled
- [ ] Input validation enabled
- [ ] CORS properly configured
- [ ] Secrets managed via environment variables
- [ ] Database user with minimal privileges
- [ ] Firewall rules configured
- [ ] VPN/Bastion host set up

### Database
- [ ] PostgreSQL encryption enabled
- [ ] Automated backups configured
- [ ] Replication enabled (for HA)
- [ ] Connection pooling configured
- [ ] Maintenance jobs scheduled
- [ ] Monitoring alerts set up

### Monitoring & Logging
- [ ] Prometheus scraping configured
- [ ] Grafana dashboards created
- [ ] Log aggregation set up (ELK, Datadog, etc.)
- [ ] Alerts configured
- [ ] Backup monitoring enabled
- [ ] Performance baselines established

### High Availability
- [ ] Load balancer configured
- [ ] Multiple replicas deployed
- [ ] Health checks configured
- [ ] Auto-scaling policies set up
- [ ] Failover tested
- [ ] Disaster recovery plan documented

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t rag-backend:${{ github.sha }} ./backend
      
      - name: Push to registry
        run: docker push rag-backend:${{ github.sha }}
      
      - name: Deploy to K8s
        run: |
          kubectl set image deployment/rag-backend \
            backend=rag-backend:${{ github.sha }} \
            -n rag-system
```

### GitLab CI

```yaml
# .gitlab-ci.yml
deploy:production:
  stage: deploy
  only:
    - main
  script:
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker push $CI_REGISTRY_IMAGE:latest
    - kubectl set image deployment/rag-backend ...
  environment:
    name: production
```

## 🔧 Troubleshooting Deployment

### Backend won't start
```bash
# Check logs
kubectl logs deployment/rag-backend -n rag-system

# Check environment variables
kubectl exec -it <pod-name> -n rag-system -- env

# Verify database connection
kubectl exec -it <pod-name> -n rag-system -- \
  python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```

### High memory usage
```bash
# Check current usage
kubectl top pods -n rag-system

# Check resource requests/limits
kubectl describe pod <pod-name> -n rag-system

# Update resource limits in deployment
kubectl set resources deployment rag-backend \
  --limits=memory=512Mi,cpu=500m \
  -n rag-system
```

### Database connection issues
```bash
# Check database connectivity
kubectl run -it --rm debug \
  --image=postgres:15 \
  --restart=Never \
  -n rag-system \
  -- psql -h postgres -U rag_user -d rag_system
```

## 📈 Post-Deployment

### Verify Deployment
```bash
# Health check
curl http://localhost:8000/api/health

# API documentation
curl http://localhost:8000/api/docs

# Metrics
curl http://localhost:9090/api/v1/targets
```

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/health

# Using hey
hey -n 1000 -c 10 http://localhost:8000/api/health

# Using Locust
locust -f locustfile.py --host=http://localhost:8000
```

### Performance Monitoring
```bash
# Monitor CPU/Memory
watch -n 1 'kubectl top pods -n rag-system'

# Monitor network
kubectl top nodes

# Check resource usage
kubectl describe nodes
```

## 🔄 Updating Deployment

### Rolling Update
```bash
# Update image
kubectl set image deployment/rag-backend \
  backend=rag-backend:v2.0 \
  -n rag-system

# Monitor rollout
kubectl rollout status deployment/rag-backend -n rag-system

# Rollback if needed
kubectl rollout undo deployment/rag-backend -n rag-system
```

### Canary Deployment
```bash
# Deploy new version as separate deployment
kubectl apply -f deployment-v2.yaml

# Route 10% traffic to new version
# Update ingress/load balancer weights

# Monitor metrics
# If healthy, gradually increase traffic
# Complete migration

# Remove old deployment
kubectl delete deployment rag-backend-v1
```

## 🆘 Disaster Recovery

### Backup Strategy
```bash
# Backup database daily
pg_dump rag_system | gzip > backup_$(date +%Y%m%d).sql.gz

# Backup vectors
# (Chroma DB automatic backups)

# Store backups offsite
aws s3 cp backup_$(date +%Y%m%d).sql.gz s3://backups/
```

### Recovery Procedure
```bash
# Stop services
kubectl scale deployment rag-backend --replicas=0 -n rag-system

# Restore database
gunzip < backup.sql.gz | psql rag_system

# Restart services
kubectl scale deployment rag-backend --replicas=3 -n rag-system

# Verify functionality
curl http://localhost:8000/api/health
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL Replication](https://www.postgresql.org/docs/current/warm-standby.html)
- [Prometheus Setup](https://prometheus.io/docs/prometheus/latest/installation/)

---

**Version**: 1.0.0  
**Last Updated**: January 2024
