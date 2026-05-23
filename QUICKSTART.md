# 🚀 Quick Start Guide

Get up and running with the Enterprise RAG System in 5 minutes!

## Prerequisites
- Docker & Docker Compose (recommended)
- OR Python 3.11+ and Node.js 18+ (for local development)

## Option 1: Docker Compose (Recommended)

### Quick Start
```bash
# Clone repository
git clone <repo-url>
cd RAG\ SYSTEM

# Start all services
docker-compose up -d

# Wait for services to be healthy
docker-compose ps

# Access the application
# Frontend: http://localhost:4200
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Configure Backend
```bash
# Edit environment variables
nano backend/.env

# Key settings to update:
# OPENAI_API_KEY=your-openai-key
# ANTHROPIC_API_KEY=your-anthropic-key (optional)
# SECRET_KEY=generate-a-random-key
```

### Test the System
```bash
# Health check
curl http://localhost:8000/api/health

# API documentation
open http://localhost:8000/api/docs

# Frontend
open http://localhost:4200
```

### View Logs
```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# All services
docker-compose logs -f
```

---

## Option 2: Local Development

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env

# Start server
uvicorn app.main:app --reload

# Available at: http://localhost:8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
ng serve

# Available at: http://localhost:4200
```

---

## First Steps

### 1. Create an Account
1. Navigate to http://localhost:4200/signup
2. Enter email and password
3. Click "Sign Up"

### 2. Upload a Document
1. Go to "Upload" tab
2. Select a PDF, Excel, or CSV file
3. Click "Upload"
4. Wait for processing to complete

### 3. Query Your Document
1. Go to "Query" tab
2. Enter a question (e.g., "What are the main findings?")
3. Click "Search"
4. View the AI-generated answer and source documents

### 4. Create an Agent Task
1. Go to "Agents" tab
2. Create new task with:
   - Task name
   - Description
   - Instructions
   - Select documents
3. Click "Create Task"
4. Monitor task execution
5. View results when complete

### 5. View Analytics
1. Go to "Analytics" tab
2. See:
   - Query statistics
   - Document analytics
   - System performance
   - Usage reports

---

## Common Commands

### Docker Compose
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f [service]

# Restart a service
docker-compose restart [service]

# Remove volumes (CAUTION: deletes data)
docker-compose down -v
```

### Backend
```bash
# Run tests
cd backend
pytest tests/

# Check code quality
flake8 app/
mypy app/

# Format code
black app/
```

### Frontend
```bash
# Build for production
ng build --configuration production

# Run tests
ng test

# Lint code
ng lint
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port in backend/.env
PORT=8001
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check database URL
docker exec rag-backend env | grep DATABASE_URL
```

### Frontend Won't Load
```bash
# Clear browser cache
Ctrl+Shift+Delete (or Cmd+Shift+Delete)

# Check if backend is running
curl http://localhost:8000/api/health

# Check console for CORS errors
# Open browser DevTools: F12
```

### Out of Memory
```bash
# Check Docker resources
docker stats

# Increase Docker memory
# Docker Desktop > Settings > Resources > Memory

# Or restart with more memory
docker-compose down
docker-compose up -d
```

---

## 📚 Next Steps

1. **Read Full Documentation**: See [README.md](../README.md)
2. **API Reference**: See [docs/API.md](../docs/API.md)
3. **Security Setup**: See [docs/SECURITY.md](../docs/SECURITY.md)
4. **Deployment**: See [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)
5. **Architecture**: See [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)

---

## 🆘 Need Help?

1. Check [README.md](../README.md) for detailed documentation
2. Review [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) for system design
3. Check logs: `docker-compose logs -f [service]`
4. Search existing issues on GitHub
5. Create new issue with error details

---

## 🎉 You're Ready!

The system is now running and ready for use. Start by uploading documents and querying them with natural language questions!

**Happy exploring! 🚀**
