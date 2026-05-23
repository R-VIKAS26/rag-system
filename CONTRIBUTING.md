# Contributing to Enterprise RAG System

Thank you for your interest in contributing! This guide will help you get started.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## How to Contribute

### 1. Report Bugs
Create an issue with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### 2. Suggest Features
Submit an issue with:
- Feature description
- Use case and benefit
- Possible implementation

### 3. Submit Code

#### Setup Development Environment
```bash
# Fork and clone repository
git clone https://github.com/your-username/rag-system.git
cd rag-system

# Create feature branch
git checkout -b feature/your-feature-name

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
```

#### Code Standards

**Python:**
- Follow PEP 8
- Use type hints
- Write docstrings
- Test coverage > 80%

**TypeScript/Angular:**
- Follow Angular style guide
- Use TSLint
- Write unit tests
- Components should have tests

#### Commit Messages
```
feat: add new feature
fix: bug fix
docs: documentation
test: tests
refactor: code refactoring
style: formatting
```

#### Testing
```bash
# Backend
cd backend
pytest tests/ --cov=app

# Frontend
cd frontend
ng test
```

#### Pull Request Process
1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG
5. Create descriptive PR with:
   - Summary of changes
   - Motivation and context
   - Testing done
   - Screenshots (if UI changes)

## Development Workflow

```
1. Fork repository
   ↓
2. Create feature branch
   ↓
3. Make changes & commit
   ↓
4. Push to fork
   ↓
5. Create Pull Request
   ↓
6. Address review comments
   ↓
7. Merge to main
```

## Community

- GitHub Issues: Report bugs and feature requests
- Discussions: Share ideas and ask questions
- Email: community@rag-system.com

Thank you for contributing! 🙏
