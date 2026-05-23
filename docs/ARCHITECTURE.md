# Architecture & Design

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                        Frontend Layer                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Angular Application (SPA)                      │   │
│  │  ┌──────────────┐  ┌──────────────────────┐    │   │
│  │  │ UI Components│  │ Services & Guards    │    │   │
│  │  ├──────────────┤  ├──────────────────────┤    │   │
│  │  │ Dashboard    │  │ AuthService          │    │   │
│  │  │ Upload       │  │ DocumentService      │    │   │
│  │  │ Query        │  │ RagService           │    │   │
│  │  │ Agents       │  │ AgentService         │    │   │
│  │  │ Analytics    │  │ AnalyticsService     │    │   │
│  │  └──────────────┘  └──────────────────────┘    │   │
│  └─────────────────────────────────────────────────┘   │
│                           │                              │
└───────────────────────────┼──────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    API Gateway Layer                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │  FastAPI App                                    │   │
│  │  ┌──────────────┐  ┌──────────────────────┐    │   │
│  │  │ Request      │  │ Response             │    │   │
│  │  │ Validation   │  │ Formatting           │    │   │
│  │  └──────────────┘  └──────────────────────┘    │   │
│  └─────────────────────────────────────────────────┘   │
│                           │                              │
└───────────────────────────┼──────────────────────────────┘
                            │
                ┌───────────┼───────────┐
                │           │           │
                ▼           ▼           ▼
┌─────────────┐ ┌────────┐ ┌───────┐ ┌──────────┐
│   Auth API  │ │Document│ │ RAG   │ │ Agents   │
│ Endpoints   │ │ API    │ │ API   │ │ API      │
└──────┬──────┘ └───┬────┘ └───┬───┘ └────┬─────┘
       │            │          │          │
       └────────────┼──────────┼──────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌─────────┐  ┌────────────┐  ┌──────────────┐
│ Services│  │   RAG      │  │   Agents     │
│ Layer   │  │   Layer    │  │   Layer      │
├─────────┤  ├────────────┤  ├──────────────┤
│ Auth    │  │Embed       │  │Agentic RAG   │
│ Document│  │Vector      │  │Task Manager  │
│ RAG     │  │Search      │  │Tool Registry │
│ LLM     │  │LLM Prompt  │  │Execution     │
└────┬────┘  └──────┬─────┘  └──────┬───────┘
     │              │               │
     └──────────────┼───────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│  PostgreSQL  │ │Chroma DB │ │  Redis       │
│  Database    │ │ Vector   │ │  Cache       │
│              │ │ Store    │ │              │
└──────────────┘ └──────────┘ └──────────────┘
```

## 🔌 Component Details

### Frontend Components

**Angular Architecture:**
- Modular component structure
- Reactive forms with validation
- Interceptors for API authentication
- Route guards for Protected pages
- HTTP error handling

**Key Components:**
- DashboardComponent: Main dashboard view
- DocumentUploadComponent: File upload interface
- QueryInterfaceComponent: RAG query UI
- AgentsComponent: Agent task management
- AnalyticsComponent: System analytics
- AuthComponents: Login/signup forms

### Backend Services

**Core Services:**
```python
AuthService         # JWT token generation/validation
DocumentService     # Document handling
RagService         # RAG logic orchestration
LLMService         # LLM API integration
EmbeddingService   # Text embeddings
VectorStoreService # Chroma DB operations
AgenticRAG         # Autonomous agent system
```

### Data Flow

#### Document Upload Flow
```
1. Frontend: User selects file
   ↓
2. Frontend: Validate file type and size
   ↓
3. Frontend: Upload to /documents/upload
   ↓
4. Backend: Validate and store file
   ↓
5. Backend: Extract text from document
   ↓
6. Backend: Chunk text (overlap: 200)
   ↓
7. Backend: Generate embeddings
   ↓
8. Backend: Store in Chroma DB
   ↓
9. Frontend: Show completion confirmation
```

#### Query Processing Flow
```
1. Frontend: User enters query
   ↓
2. Frontend: Send to /rag/query
   ↓
3. Backend: Generate query embedding
   ↓
4. Backend: Search Chroma DB (top_k=5)
   ↓
5. Backend: Build context from results
   ↓
6. Backend: Call LLM with context
   ↓
7. Backend: Return answer + sources
   ↓
8. Frontend: Display results
```

#### Agent Task Flow
```
1. Frontend: User creates agent task
   ↓
2. Backend: Initialize AgenticRAG
   ↓
3. Backend: Task.start()
   ↓
4. Backend: Retrieve documents
   ↓
5. Backend: Analyze documents
   ↓
6. Backend: Extract insights
   ↓
7. Backend: Generate summary
   ↓
8. Backend: Task.complete()
   ↓
9. Frontend: Display results
```

## 📊 Database Schema

### PostgreSQL Tables

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  hashed_password VARCHAR NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Documents
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  filename VARCHAR NOT NULL,
  file_type VARCHAR,
  file_size INTEGER,
  content TEXT,
  status VARCHAR,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Embeddings (Aurora/Vector DB)
CREATE TABLE embeddings (
  id UUID PRIMARY KEY,
  document_id UUID REFERENCES documents(id),
  content TEXT,
  embedding vector(1536),  -- 1536 dimensions for text-embedding-3-small
  metadata JSONB,
  created_at TIMESTAMP
);

-- Audit Log
CREATE TABLE audit_log (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  action VARCHAR,
  resource_type VARCHAR,
  resource_id VARCHAR,
  details JSONB,
  created_at TIMESTAMP
);

-- Agent Tasks
CREATE TABLE agent_tasks (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR,
  description TEXT,
  status VARCHAR,
  result JSONB,
  execution_time FLOAT,
  created_at TIMESTAMP,
  completed_at TIMESTAMP
);
```

## 🔐 Authentication Flow

```
┌──────────────┐                          ┌──────────────┐
│   Client     │                          │   Backend    │
└──────┬───────┘                          └──────┬───────┘
       │                                         │
       │──────── POST /auth/login ─────────────>│
       │ {email, password}                      │
       │                                        │ Validate
       │                                        │ Hash password
       │<───── 200 OK ──────────────────────────│
       │ {access_token, expires_in}            │
       │                                        │
       │──── GET /documents/ ──────────────────>│
       │ Authorization: Bearer {token}         │
       │                                        │ Verify JWT
       │                                        │ Extract user_id
       │<─── 200 OK ───────────────────────────│
       │ [documents]                           │

```

## 🔄 Agentic RAG Task Cycle

```
┌────────────────────────────────────────┐
│     Initialize Agent Task               │
├────────────────────────────────────────┤
│ - Create task with instructions        │
│ - Load user documents                  │
│ - Initialize tools                     │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│     Analyze Query/Instructions          │
├────────────────────────────────────────┤
│ - Break down instructions              │
│ - Identify required tools              │
│ - Plan execution steps                 │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│     Retrieve Documents                  │
├────────────────────────────────────────┤
│ - Perform vector search                │
│ - Rank by relevance                    │
│ - Select top_k documents               │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│     Process & Analyze                   │
├────────────────────────────────────────┤
│ - Extract entities                     │
│ - Identify patterns                    │
│ - Calculate metrics                    │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│     Generate Results                    │
├────────────────────────────────────────┤
│ - Summary generation                   │
│ - Insight extraction                   │
│ - Recommendation generation            │
└────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────┐
│     Return Results                      │
├────────────────────────────────────────┤
│ - Compile output                       │
│ - Format response                      │
│ - Record metrics                       │
└────────────────────────────────────────┘
```

## 📡 Integration Points

### External APIs
- **OpenAI**: GPT-4, GPT-3.5-turbo, Embeddings
- **Anthropic**: Claude models
- **Other LLMs**: Via LangChain

### Data Stores
- **PostgreSQL**: Primary database
- **Redis**: Caching and sessions
- **Chroma DB**: Vector embeddings
- **S3/GCS**: Document storage (optional)

### Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **ELK Stack**: Log aggregation (optional)

## 🚀 Scalability Patterns

### Horizontal Scaling
- Load balancer distributes requests
- Multiple API instances
- Shared database and cache
- Session affinity not required (stateless)

### Vertical Scaling
- Increase container resources (memory, CPU)
- Database connection pooling
- Caching optimization

### Database Scaling
- Read replicas for analytics
- Connection pooling
- Proper indexing on frequently queried fields

## 🔄 Deployment Patterns

### Blue-Green Deployment
```
1. Deploy v2 (green) alongside v1 (blue)
2. Route 0% traffic to green
3. Run health checks
4. Switch 100% traffic to green
5. Keep blue for rollback
```

### Canary Deployment
```
1. Deploy v2 to small subset (5%)
2. Monitor metrics
3. Gradually increase traffic (10%, 25%, 50%, 100%)
4. Rollback if issues detected
```

### Rolling Update
```
1. Update 1 of N replicas
2. Wait for health checks
3. Move to next replica
4. Continue until all updated
```

## 📚 Caching Strategy

### Frontend Caching
- Service worker for offline support
- LocalStorage for user preferences
- HTTP caching headers

### Backend Caching
- Query results in Redis (TTL: 1 hour)
- Embedding cache (TTL: 7 days)
- LLM response cache (TTL: 1 day)

## 🎯 Performance Optimization

### Query Optimization
- Database query indexing
- Connection pooling
- Query result caching

### API Optimization
- Response compression (gzip)
- Pagination for large datasets
- Lazy loading on frontend

### Vector Search Optimization
- Approximate nearest neighbor search
- Index optimization
- Batch operations

---

**Version**: 1.0.0  
**Last Updated**: January 2024
