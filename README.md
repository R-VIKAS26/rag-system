# Enterprise RAG System - Comprehensive Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [API Documentation](#api-documentation)
7. [Deployment](#deployment)
8. [Security](#security)
9. [Monitoring](#monitoring)
10. [Troubleshooting](#troubleshooting)

## 🎯 Overview

**Enterprise RAG System** is a production-ready Retrieval-Augmented Generation (RAG) platform with:

- **Agentic RAG**: Autonomous agents for document analysis
- **Multi-format Support**: PDF, Excel, CSV, JSON, and more
- **Vector Search**: Chroma DB for semantic similarity search
- **LLM Integration**: OpenAI, Anthropic, and other models
- **Enterprise Security**: ADA compliance, encryption, audit logging
- **Modern UI**: Angular frontend with responsive design
- **CI/CD Pipeline**: GitHub Actions with automated testing
- **Scalability**: Kubernetes-ready deployment
- **Monitoring**: Prometheus + Grafana observability

## 🏗️ Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                   Enterprise RAG System                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────┐         ┌──────────────────┐       │
│  │  Angular UI/UX  │         │  API Gateway     │       │
│  │  (Port 4200)    │         │  (Port 8000)     │       │
│  └────────┬────────┘         └────────┬─────────┘       │
│           │                           │                  │
│           └───────────────┬───────────┘                  │
│                           │                              │
│           ┌───────────────▼──────────────┐               │
│           │    FastAPI Backend           │               │
│           │  ┌──────────────────────┐   │               │
│           │  │ - Authentication     │   │               │
│           │  │ - RAG Processing     │   │               │
│           │  │ - Agentic System     │   │               │
│           │  │ - Document Upload    │   │               │
│           │  └──────────────────────┘   │               │
│           └───────────────┬──────────────┘               │
│                           │                              │
│        ┌──────────────────┼──────────────────┐           │
│        │                  │                  │           │
│   ┌────▼────┐      ┌─────▼─────┐    ┌─────▼─────┐     │
│   │ChromaDB  │      │PostgreSQL  │    │Redis Cache│     │
│   │Vector DB │      │Database    │    │Session    │     │
│   │(Port 8001)      │(Port 5432) │    │(Port 6379)│     │
│   └──────────┘      └────────────┘    └───────────┘     │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │    Monitoring Stack                             │    │
│  │  ┌──────────┐  ┌─────────┐  ┌──────────────┐  │    │
│  │  │Prometheus│  │ Grafana │  │ Alert Manager│  │    │
│  │  │(Port 9090)  │(Port 3000) │              │  │    │
│  │  └──────────┘  └─────────┘  └──────────────┘  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Features

### Core RAG Capabilities
- **Document Ingestion**: Upload and process PDFs, Excel, CSV, JSON
- **Vector Embeddings**: Text-embedding-3-small with Chroma DB
- **Semantic Search**: Find relevant documents using similarity
- **LLM Integration**: GPT-4, GPT-3.5-turbo, Claude support
- **Context Awareness**: Pass retrieved context to LLM

### Agentic Features
- **Autonomous Agents**: Task-oriented document analysis
- **Tool Integration**: Pre-built tools for analysis and extraction
- **Multi-step Reasoning**: Complex task decomposition
- **Progress Tracking**: Real-time task execution monitoring
- **Result Compilation**: Structured output generation

### Security & Compliance
- **JWT Authentication**: Secure token-based access
- **ADA Compliance**: Accessibility and compliance features
- **Encryption**: Data encryption at rest and in transit
- **Audit Logging**: Complete audit trail for compliance
- **Rate Limiting**: Protection against abuse
- **Input Validation**: Comprehensive input validation

### Enterprise Features
- **Multi-tenant Ready**: Isolated user workspaces
- **Role-based Access**: Different permission levels
- **Audit Trail**: Complete action logging
- **Backup & Recovery**: Data persistence and recovery
- **High Availability**: Horizontal scaling support

## 💻 Installation

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL (optional, included in Docker)
- Redis (optional, included in Docker)

### Quick Start with Docker

```bash
# Clone repository
git clone <repo-url>
cd RAG\ SYSTEM

# Start all services
docker-compose up -d

# Wait for all services to be healthy
docker-compose ps

# Backend will be available at: http://localhost:8000
# Frontend will be available at: http://localhost:4200
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
```

### Local Development Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with your configuration
# OPENAI_API_KEY=your-key
# DATABASE_URL=postgresql://...

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
ng serve

# Frontend will be available at http://localhost:4200
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in backend directory:

```bash
# FastAPI
ENVIRONMENT=development
DEBUG=True
API_TITLE=Enterprise RAG System
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://rag_user:rag_password@localhost:5432/rag_system

# Redis
REDIS_URL=redis://localhost:6379/0

# Chroma DB
CHROMA_DB_PATH=./chroma_db
CHROMA_HOST=localhost
CHROMA_PORT=8001

# LLM Models
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
ANTHROPIC_API_KEY=sk-ant-...

# Embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536

# Document Processing
MAX_UPLOAD_SIZE=52428800
ALLOWED_EXTENSIONS=pdf,docx,xlsx,csv,txt,json

# RAG Settings
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_TOP_K=5
MAX_TOKENS=2000

# Security & Compliance
ENABLE_ADA_COMPLIANCE=True
AUDIT_LOG_ENABLED=True
ENCRYPTION_ENABLED=True

# CORS
CORS_ORIGINS=["http://localhost:4200"]
```

## 📚 API Documentation

### Authentication

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Document Management

#### Upload Document
```bash
POST /api/documents/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <binary_file>

Response:
{
  "document_id": "doc_1234567890",
  "filename": "example.pdf",
  "status": "processing",
  "message": "Document received and processing started"
}
```

#### List Documents
```bash
GET /api/documents/?skip=0&limit=10
Authorization: Bearer <token>

Response:
{
  "documents": [
    {
      "document_id": "doc_123",
      "filename": "example.pdf",
      "file_type": "pdf",
      "file_size": 1024000,
      "upload_date": "2024-01-15T10:30:00",
      "status": "processed"
    }
  ],
  "total": 1
}
```

### RAG Queries

#### Query RAG System
```bash
POST /api/rag/query
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "What are the main findings?",
  "top_k": 5
}

Response:
{
  "query": "What are the main findings?",
  "answer": "Based on the documents...",
  "results": [
    {
      "content": "Relevant document excerpt...",
      "score": 0.95,
      "source": "document_1",
      "metadata": {"page": 1}
    }
  ],
  "processing_time": 1.23,
  "model_used": "gpt-4"
}
```

### Agentic Tasks

#### Create Agent Task
```bash
POST /api/agents/create-task
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Document Analysis",
  "description": "Analyze uploaded documents",
  "instructions": "Extract key insights and generate summary",
  "documents": ["doc_123", "doc_456"]
}

Response:
{
  "task_id": "task_1234567890",
  "status": "initialized",
  "result": {"message": "Agent task initialized"},
  "execution_time": 0.0,
  "iterations": 0
}
```

#### Get Task Status
```bash
GET /api/agents/task/{task_id}
Authorization: Bearer <token>

Response:
{
  "task_id": "task_123",
  "status": "running",
  "progress": 40,
  "current_action": "Analyzing documents..."
}
```

## 🚢 Deployment

### Docker Compose (Development)
```bash
docker-compose up -d
```

### Kubernetes Deployment

```bash
# Create namespace
kubectl apply -f infrastructure/k8s-config.yaml

# Deploy backend
kubectl apply -f infrastructure/k8s-backend.yaml

# Check deployment
kubectl get pods -n rag-system
kubectl get services -n rag-system
```

### Production Deployment Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Configure production database URL
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS origins
- [ ] Enable backup schedules
- [ ] Set up monitoring alerts
- [ ] Configure log aggregation
- [ ] Test disaster recovery
- [ ] Review security policies
- [ ] Set up automatic scaling

## 🔒 Security

### ADA Protocol Features

1. **Data Encryption**
   - At-rest encryption for sensitive data
   - TLS 1.3 for in-transit data
   - Key rotation policies

2. **Access Control**
   - JWT-based authentication
   - Role-based access control (RBAC)
   - Fine-grained permissions

3. **Audit Logging**
   - Complete action audit trail
   - User activity tracking
   - Compliance reporting

4. **Compliance**
   - GDPR compliance features
   - Data residency control
   - Consent management

### Best Practices

- Rotate API keys regularly
- Use strong passwords (min. 12 characters)
- Enable 2FA for admin accounts
- Regular security audits
- Penetration testing
- Dependency scanning

## 📊 Monitoring

### Prometheus Metrics

- `rag_api_requests_total`: Total API requests
- `rag_api_request_duration_seconds`: Request latency
- `rag_query_latency_seconds`: Query processing time
- `rag_documents_total`: Total documents
- `rag_vector_store_size_bytes`: Vector store size
- `rag_agent_tasks_active`: Running agent tasks
- `rag_llm_tokens_used_total`: LLM token usage

### Grafana Dashboards

Pre-built dashboards for:
- System Health
- API Performance
- Query Analytics
- Agent Task Tracking
- Resource Utilization
- Error Rates

Access Grafana at: `http://localhost:3000` (admin/admin)

## 🐛 Troubleshooting

### Common Issues

#### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Verify database connection
docker-compose exec backend python -c "import sqlalchemy; print('OK')"

# Check environment variables
docker-compose exec backend env | grep DATABASE
```

#### Frontend not connecting to backend
```bash
# Verify API URL in environment.ts
# Check CORS settings in backend
# Verify backend is running: curl http://localhost:8000/api/health
```

#### Chroma DB connection issues
```bash
# Check Chroma status
curl http://localhost:8001/api/v1/heartbeat

# Re-initialize Chroma
docker-compose down chroma
docker-compose up -d chroma
```

#### Memory issues
```bash
# Check memory usage
docker stats

# Increase Docker resources
# Edit docker-compose.yml resources section
```

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Angular Documentation](https://angular.io)
- [Chroma DB Docs](https://docs.trychroma.com)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs)

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review GitHub Issues
3. Check logs: `docker-compose logs -f [service]`
4. Contact: support@rag-system.com

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Status**: Production Ready
