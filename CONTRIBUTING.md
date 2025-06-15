# Contributing to ResearchHub API

Thank you for your interest in contributing to ResearchHub API! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git
- PostgreSQL (optional, SQLite supported)
- Basic knowledge of Django and REST APIs

### Development Setup

1. **Fork and Clone**
\`\`\`bash
git clone https://github.com/your-username/researchhub-api_4.2-lesson.git
cd researchhub-api_4.2-lesson
\`\`\`

2. **Set up Environment**
\`\`\`bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements/development.txt
\`\`\`

3. **Configure Environment**
\`\`\`bash
cp .env-example.txt .env
# Edit .env with your settings
\`\`\`

4. **Database Setup**
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
\`\`\`

5. **Run Tests**
\`\`\`bash
python manage.py test
\`\`\`

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 style guide
- Use Black for code formatting: `black .`
- Sort imports with isort: `isort .`
- Lint with flake8: `flake8 .`

### Commit Messages
Use conventional commit format:
\`\`\`
type(scope): description

feat(users): add email verification
fix(api): resolve authentication bug
docs(readme): update installation guide
test(models): add user model tests
\`\`\`

### Branch Naming
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation
- `test/test-description` - Tests only
- `refactor/refactor-description` - Code refactoring

## 🧪 Testing

### Running Tests
\`\`\`bash
# All tests
python manage.py test

# Specific app
python manage.py test apps.users

# With coverage
coverage run --source='.' manage.py test
coverage report
\`\`\`

### Writing Tests
- Write tests for all new features
- Maintain test coverage above 80%
- Use Django's TestCase for database tests
- Use factory_boy for test data generation

Example:
```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
