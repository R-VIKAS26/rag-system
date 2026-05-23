# RAG System Project Structure

## 📁 Directory Overview

```
RAG SYSTEM/
├── .github/
│   └── workflows/
│       ├── backend-ci.yml          # Backend CI/CD pipeline
│       └── frontend-ci.yml         # Frontend CI/CD pipeline
│
├── backend/
│   ├── app/
│   │   ├── api/                    # API endpoints
│   │   │   ├── health.py           # Health check endpoints
│   │   │   ├── auth.py             # Authentication routes
│   │   │   ├── documents.py        # Document management
│   │   │   ├── rag.py              # RAG query endpoints
│   │   │   ├── agents.py           # Agentic RAG endpoints
│   │   │   └── analytics.py        # Analytics endpoints
│   │   │
│   │   ├── core/                   # Core configuration
│   │   │   ├── config.py           # Settings management
│   │   │   └── security.py         # Security utilities
│   │   │
│   │   ├── services/               # Business logic services
│   │   │   ├── vector_store.py     # Chroma DB wrapper
│   │   │   ├── embedding_service.py # Embeddings
│   │   │   ├── rag_service.py      # RAG logic
│   │   │   └── llm_service.py      # LLM integration
│   │   │
│   │   ├── agents/                 # Agentic RAG system
│   │   │   └── agentic_rag.py      # Agent implementation
│   │   │
│   │   ├── models/                 # Data models
│   │   ├── utils/                  # Utility functions
│   │   │   ├── logging.py          # Logging setup
│   │   │   ├── monitoring.py       # Prometheus metrics
│   │   │   ├── error_handlers.py   # Error handling
│   │   │   └── document_processor.py # File processing
│   │   │
│   │   └── main.py                 # FastAPI app entry point
│   │
│   ├── tests/                      # Unit and integration tests
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment variables template
│   ├── Dockerfile                  # Docker image
│   └── alembic/                    # Database migrations
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/         # Angular components
│   │   │   │   ├── dashboard/
│   │   │   │   ├── document-upload/
│   │   │   │   ├── query-interface/
│   │   │   │   ├── agents/
│   │   │   │   ├── analytics/
│   │   │   │   ├── settings/
│   │   │   │   └── auth/
│   │   │   │
│   │   │   ├── services/           # Angular services
│   │   │   │   ├── auth.service.ts
│   │   │   │   ├── document.service.ts
│   │   │   │   ├── rag.service.ts
│   │   │   │   ├── agent.service.ts
│   │   │   │   └── analytics.service.ts
│   │   │   │
│   │   │   ├── models/             # TypeScript models
│   │   │   ├── guards/             # Route guards
│   │   │   │   └── auth.guard.ts
│   │   │   ├── interceptors/       # HTTP interceptors
│   │   │   │   └── auth.interceptor.ts
│   │   │   │
│   │   │   ├── app.module.ts       # Root module
│   │   │   ├── app-routing.module.ts # Routing
│   │   │   ├── app.component.ts    # Root component
│   │   │   ├── app.component.html
│   │   │   └── app.component.css
│   │   │
│   │   ├── assets/                 # Static assets
│   │   ├── styles/                 # Global styles
│   │   ├── environments/           # Environment configs
│   │   ├── index.html
│   │   └── main.ts
│   │
│   ├── package.json
│   ├── angular.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── Dockerfile.dev
│
├── infrastructure/
│   ├── prometheus.yml              # Prometheus config
│   ├── k8s-config.yaml             # K8s namespace & secrets
│   ├── k8s-backend.yaml            # K8s backend deployment
│   └── nginx.conf                  # Nginx config
│
├── docs/
│   ├── API.md                      # API documentation
│   ├── ARCHITECTURE.md             # Architecture docs
│   ├── DEPLOYMENT.md               # Deployment guide
│   └── SECURITY.md                 # Security guidelines
│
├── docker-compose.yml              # Multi-container setup
├── .gitignore
├── README.md                       # Main documentation
└── LICENSE

```

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI application entry point |
| `backend/app/core/config.py` | Settings and configuration |
| `backend/app/services/rag_service.py` | Core RAG logic |
| `backend/app/agents/agentic_rag.py` | Autonomous agent system |
| `frontend/src/app/app.module.ts` | Angular root module |
| `docker-compose.yml` | Local development stack |
| `.github/workflows/backend-ci.yml` | CI/CD pipeline |

## 📦 Service Ports

| Service | Port | Purpose |
|---------|------|---------|
| FastAPI Backend | 8000 | API endpoints |
| Angular Frontend | 4200 | Web UI |
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Cache & sessions |
| Chroma DB | 8001 | Vector store |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Dashboard & visualization |

## 🚀 Quick Start

```bash
# Start all services
docker-compose up -d

# Backend API: http://localhost:8000
# Frontend UI: http://localhost:4200
# API Docs: http://localhost:8000/api/docs
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
```

## 📚 Documentation Files

- [README.md](./README.md) - Main documentation
- [docs/API.md](./docs/API.md) - API reference
- [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) - System architecture
- [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) - Deployment guide
- [docs/SECURITY.md](./docs/SECURITY.md) - Security guidelines
