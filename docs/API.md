# API Reference Guide

## 🔐 Authentication Endpoints

### POST /api/auth/login
Authenticate user and receive JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Errors:**
- `401`: Invalid credentials
- `400`: Validation error

---

### POST /api/auth/signup
Create new user account.

**Request:**
```json
{
  "email": "newuser@example.com",
  "password": "secure_password"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### POST /api/auth/logout
Logout current user.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "message": "Successfully logged out"
}
```

---

### GET /api/auth/me
Get current authenticated user.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "user_id": "user_123",
  "email": "user@example.com"
}
```

---

## 📄 Document Endpoints

### POST /api/documents/upload
Upload a new document.

**Headers:**
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (required): File to upload (PDF, Excel, CSV, etc.)

**Response (201):**
```json
{
  "document_id": "doc_1704067800.5",
  "filename": "report.pdf",
  "status": "processing",
  "message": "Document received and processing started"
}
```

**Errors:**
- `400`: Invalid file type
- `413`: File too large
- `401`: Unauthorized

---

### GET /api/documents/
List all documents.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `skip` (optional): Number of documents to skip (default: 0)
- `limit` (optional): Max documents to return (default: 10)

**Response (200):**
```json
{
  "documents": [
    {
      "document_id": "doc_123",
      "filename": "report.pdf",
      "file_type": "pdf",
      "file_size": 2048576,
      "upload_date": "2024-01-15T10:30:00",
      "status": "processed"
    }
  ],
  "total": 1
}
```

---

### GET /api/documents/{document_id}
Get specific document details.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "document_id": "doc_123",
  "filename": "report.pdf",
  "file_type": "pdf",
  "file_size": 2048576,
  "upload_date": "2024-01-15T10:30:00",
  "status": "processed"
}
```

**Errors:**
- `404`: Document not found

---

### DELETE /api/documents/{document_id}
Delete a document.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (204):** No content

**Errors:**
- `404`: Document not found

---

## 🔍 RAG Query Endpoints

### POST /api/rag/query
Query RAG system with natural language question.

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "query": "What are the main findings?",
  "document_ids": ["doc_123", "doc_456"],
  "top_k": 5
}
```

**Response (200):**
```json
{
  "query": "What are the main findings?",
  "answer": "Based on the retrieved documents, the main findings are...",
  "results": [
    {
      "content": "Relevant document excerpt...",
      "score": 0.95,
      "source": "doc_123",
      "metadata": {
        "page": 1,
        "chunk_id": "chunk_1"
      }
    }
  ],
  "processing_time": 2.34,
  "model_used": "gpt-4"
}
```

**Errors:**
- `400`: Empty query
- `401`: Unauthorized

---

### POST /api/rag/chat
Multi-turn conversation with RAG system.

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "query": "Tell me more about that point",
  "document_ids": ["doc_123"]
}
```

**Response:** Same format as `/query`

---

### GET /api/rag/search
Search documents using vector similarity.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `query` (required): Search query
- `top_k` (optional): Number of results (default: 5)

**Response (200):**
```json
[
  {
    "content": "Matching document content...",
    "score": 0.92,
    "metadata": {
      "source": "doc_123",
      "page": 1
    }
  }
]
```

---

## 🤖 Agent Endpoints

### POST /api/agents/create-task
Create autonomous agent task.

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "name": "Document Analysis",
  "description": "Analyze uploaded documents for insights",
  "instructions": "Extract key findings and create summary",
  "documents": ["doc_123", "doc_456"]
}
```

**Response (201):**
```json
{
  "task_id": "task_1704067800.5",
  "status": "initialized",
  "result": {
    "message": "Agent task initialized"
  },
  "execution_time": 0.0,
  "iterations": 0
}
```

---

### GET /api/agents/task/{task_id}
Get agent task status.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "task_id": "task_123",
  "status": "running",
  "progress": 45,
  "current_action": "Extracting entities from documents...",
  "iterations": 2
}
```

---

### GET /api/agents/task/{task_id}/result
Get completed task result.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "task_id": "task_123",
  "result": {
    "task_name": "Document Analysis",
    "summary": "Overall summary of findings...",
    "insights": {
      "insights": "Key insights identified...",
      "patterns": ["Pattern 1", "Pattern 2"]
    },
    "documents_analyzed": 2,
    "iterations": 5
  },
  "execution_time": 45.67,
  "iterations": 5
}
```

**Errors:**
- `404`: Task not found or not completed

---

### POST /api/agents/task/{task_id}/cancel
Cancel running agent task.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "message": "Task task_123 cancelled"
}
```

---

### GET /api/agents/available-tools
List available agent tools.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "tools": [
    {
      "name": "analyze_document",
      "description": "Analyze document content",
      "parameters": ["document_id", "query"]
    },
    {
      "name": "search_documents",
      "description": "Search documents using vector similarity",
      "parameters": ["query", "top_k"]
    },
    {
      "name": "generate_summary",
      "description": "Generate summary of documents",
      "parameters": ["document_ids"]
    },
    {
      "name": "extract_entities",
      "description": "Extract named entities from documents",
      "parameters": ["document_id"]
    }
  ]
}
```

---

## 📊 Analytics Endpoints

### GET /api/analytics/user-stats
Get user activity statistics.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "total_queries": 42,
  "total_documents": 15,
  "total_time_spent": 3600.5,
  "average_query_time": 2.34,
  "last_activity": "2024-01-15T14:30:00"
}
```

---

### GET /api/analytics/system-metrics
Get system performance metrics.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `metric` (optional): Metric name (default: "requests_per_minute")
- `period_hours` (optional): Time period in hours (default: 24)

**Response (200):**
```json
{
  "metric": "requests_per_minute",
  "data": [
    {
      "timestamp": "2024-01-15T10:00:00",
      "value": 45.5,
      "label": "RPM"
    }
  ],
  "summary": {
    "average": 42.3,
    "max": 98.5,
    "min": 12.3
  }
}
```

---

### GET /api/analytics/rag-performance
Get RAG system performance metrics.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "average_query_time": 2.45,
  "average_accuracy": 0.87,
  "total_queries": 156,
  "cache_hit_rate": 0.65,
  "model_latency": 1.23
}
```

---

### GET /api/analytics/document-analytics
Get document statistics.

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `document_id` (optional): Specific document ID

**Response (200):**
```json
{
  "total_documents": 15,
  "total_size": 524288000,
  "documents_by_type": {
    "pdf": 8,
    "xlsx": 4,
    "csv": 3
  },
  "most_queried": [
    "doc_123",
    "doc_456"
  ],
  "indexing_status": {
    "indexed": 15,
    "pending": 0,
    "failed": 0
  }
}
```

---

## ✅ Health Check Endpoints

### GET /api/health/
General health check.

**Response (200):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

---

### GET /api/health/live
Kubernetes liveness probe.

**Response (200):**
```json
{
  "status": "alive"
}
```

---

### GET /api/health/ready
Kubernetes readiness probe.

**Response (200):**
```json
{
  "status": "ready"
}
```

---

## 🔑 Authentication

All endpoints except `/auth/login` and `/auth/signup` require JWT token in header:

```
Authorization: Bearer <token>
```

Tokens expire after 30 minutes by default. Use `/auth/refresh` to get new token.

---

## ❌ Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message",
  "type": "ErrorType"
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

## 📈 Rate Limiting

- Default: 100 requests per hour per user
- Configurable via `RATE_LIMIT_REQUESTS` setting
- Returns `429` status when exceeded

---

## 📚 Additional Resources

- [OpenAPI/Swagger Docs](http://localhost:8000/api/docs)
- [ReDoc Documentation](http://localhost:8000/api/redoc)
- [Main README](../README.md)
