# 🧬 ResearchHub API

A comprehensive Django REST API for collaborative scientific research management platform. This API enables researchers to manage projects, experiments, findings, publications, and collaborate with other researchers worldwide.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-v4.2+-green.svg)
![DRF](https://img.shields.io/badge/djangorestframework-v3.14+-red.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-v13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### 🔐 Authentication & User Management
- JWT-based authentication
- Email verification system
- Password reset functionality
- User profiles with ORCID integration
- Role-based permissions (Admin, Moderator, Researcher)

### 👥 Social Features
- Follow/unfollow researchers
- Direct messaging system
- Real-time notifications
- Comment system with nested replies
- Like/unlike functionality

### 🔬 Research Management
- **Research Groups**: Create and manage research teams
- **Projects**: Organize research projects with funding tracking
- **Experiments**: Document experimental procedures and methodologies
- **Findings**: Record and share research results
- **Publications**: Manage academic publications with citation tracking

### 📁 File Management
- File upload system for research data
- Support for documents, images, datasets, and code
- Attachment system for findings and experiments

### 🔍 Search & Discovery
- Global search across all resources
- Tag-based categorization
- Advanced filtering and sorting
- Analytics and reporting dashboard

### 📊 Analytics
- User activity tracking
- Research impact metrics
- Citation counting
- View and download statistics

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 13+ (optional, SQLite supported for development)
- Redis (optional, for caching and background tasks)

### Installation

1. **Clone the repository**
\`\`\`bash
git clone https://github.com/070DBEK/researchhub-api_4.2-lesson.git
cd researchhub-api_4.2-lesson
\`\`\`

2. **Create virtual environment**
\`\`\`bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
\`\`\`

3. **Install dependencies**
\`\`\`bash
# Development
pip install -r requirements/development.txt
# Production
pip install -r requirements/production.txt
\`\`\`

4. **Environment setup**
\`\`\`bash
# Copy environment template
cp .env-example.txt .env
# Edit .env file with your settings
\`\`\`

5. **Database setup**
\`\`\`bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
\`\`\`

6. **Run the server**
\`\`\`bash
python manage.py runserver
\`\`\`

### 🐳 Docker Setup

\`\`\`bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d
\`\`\`

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Admin Panel**: http://localhost:8000/admin/

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

\`\`\`env
# Django Settings
DJANGO_ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
USE_SQLITE=True

# Database (PostgreSQL for production)
# DB_NAME=researchhub
# DB_USER=postgres
# DB_PASSWORD=password
# DB_HOST=localhost
# DB_PORT=5432

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# URLs
SITE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Redis (optional)
REDIS_URL=redis://localhost:6379
\`\`\`

### Settings Structure

The project uses environment-specific settings:

\`\`\`
config/settings/
├── __init__.py          # Auto-detects environment
├── base.py             # Common settings
├── development.py      # Development settings
└── production.py       # Production settings
\`\`\`

## 📚 API Endpoints

### Authentication
\`\`\`
POST /api/v1/auth/register/          # User registration
POST /api/v1/auth/login/             # User login
POST /api/v1/auth/logout/            # User logout
POST /api/v1/auth/verify-email/      # Email verification
POST /api/v1/auth/password-reset/    # Password reset request
POST /api/v1/auth/token/refresh/     # JWT token refresh
\`\`\`

### Core Resources
\`\`\`
GET  /api/v1/users/                  # List users
GET  /api/v1/users/{id}/             # User detail
GET  /api/v1/users/me/               # Current user profile

GET  /api/v1/research-groups/        # List research groups
POST /api/v1/research-groups/        # Create research group
GET  /api/v1/research-groups/{id}/   # Research group detail

GET  /api/v1/projects/               # List projects
POST /api/v1/projects/               # Create project
GET  /api/v1/projects/{id}/          # Project detail

GET  /api/v1/experiments/            # List experiments
POST /api/v1/experiments/            # Create experiment
GET  /api/v1/experiments/{id}/       # Experiment detail

GET  /api/v1/findings/               # List findings
POST /api/v1/findings/               # Create finding
GET  /api/v1/findings/{id}/          # Finding detail

GET  /api/v1/publications/           # List publications
POST /api/v1/publications/           # Create publication
GET  /api/v1/publications/{id}/      # Publication detail
\`\`\`

### Social Features
\`\`\`
POST /api/v1/profiles/{id}/follow/   # Follow user
POST /api/v1/profiles/{id}/unfollow/ # Unfollow user

GET  /api/v1/messages/               # List messages
POST /api/v1/messages/               # Send message

GET  /api/v1/notifications/          # List notifications
POST /api/v1/notifications/{id}/mark-as-read/ # Mark as read

POST /api/v1/findings/{id}/like/     # Like finding
POST /api/v1/findings/{id}/unlike/   # Unlike finding
\`\`\`

### Search & Discovery
\`\`\`
GET  /api/v1/search/?q=query         # Global search
GET  /api/v1/tags/                   # List tags
GET  /api/v1/analytics/summary/      # Analytics dashboard
\`\`\`

## 🏗️ Project Structure

\`\`\`
researchhub-api/
├── apps/
│   ├── common/              # Shared utilities and base classes
│   ├── users/               # User management and authentication
│   ├── profiles/            # User profiles and social features
│   ├── research_groups/     # Research group management
│   ├── projects/            # Project management
│   ├── experiments/         # Experiment tracking
│   ├── findings/            # Research findings
│   ├── attachments/         # File upload and management
│   ├── publications/        # Publication management
│   ├── comments/            # Comment system
│   ├── likes/               # Like/unlike functionality
│   ├── messages/            # Direct messaging
│   ├── notifications/       # Notification system
│   ├── analytics/           # Analytics and reporting
│   └── tags/                # Tagging and search
├── config/
│   ├── settings/            # Environment-specific settings
│   ├── urls.py              # URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── requirements/
│   ├── base.txt             # Base dependencies
│   ├── development.txt      # Development dependencies
│   └── production.txt       # Production dependencies
├── scripts/
│   └── setup.sh             # Setup script
├── docker-compose.yml       # Docker configuration
├── Dockerfile               # Docker image
└── manage.py                # Django management script
\`\`\`

## 🧪 Testing

\`\`\`bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Run specific app tests
python manage.py test apps.users
\`\`\`

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**
\`\`\`bash
export DJANGO_ENVIRONMENT=production
export SECRET_KEY=your-production-secret-key
export DEBUG=False
export ALLOWED_HOSTS=yourdomain.com
\`\`\`

2. **Database Migration**
\`\`\`bash
python manage.py migrate
python manage.py collectstatic
\`\`\`

3. **Web Server**
\`\`\`bash
# Using Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Using uWSGI
uwsgi --http :8000 --module config.wsgi
\`\`\`

### Docker Production

\`\`\`bash
# Build production image
docker build -t researchhub-api .

# Run with environment variables
docker run -p 8000:8000 --env-file .env researchhub-api
\`\`\`

### Cloud Deployment

The API is ready for deployment on:
- **Heroku**: Use `Procfile` and `runtime.txt`
- **AWS**: Use Elastic Beanstalk or ECS
- **Google Cloud**: Use App Engine or Cloud Run
- **DigitalOcean**: Use App Platform

## 🔧 Development

### Code Quality

\`\`\`bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
\`\`\`

### Pre-commit Hooks

\`\`\`bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
\`\`\`

### Database Management

\`\`\`bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database
python manage.py flush

# Load sample data
python manage.py loaddata fixtures/sample_data.json
\`\`\`

## 📊 Performance

### Optimization Features

- **Database**: Optimized queries with select_related and prefetch_related
- **Caching**: Redis-based caching for frequently accessed data
- **Pagination**: Efficient pagination for large datasets
- **Indexing**: Database indexes on frequently queried fields
- **Compression**: Static file compression with WhiteNoise

### Monitoring

- **Logging**: Comprehensive logging system
- **Error Tracking**: Sentry integration for production
- **Performance**: Django Debug Toolbar for development
- **Health Checks**: Built-in health check endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages
- Keep pull requests focused and small

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django REST Framework team for the excellent framework
- PostgreSQL community for the robust database
- All contributors who helped improve this project

## 📞 Support

- **Documentation**: [API Docs](http://localhost:8000/api/docs/)
- **Issues**: [GitHub Issues](https://github.com/070DBEK/researchhub-api_4.2-lesson/issues)
- **Email**: ahmadovozodbek80@gmail.com

## 🗺️ Roadmap

### Version 2.0
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard
- [ ] Machine learning recommendations
- [ ] Mobile app API extensions
- [ ] GraphQL API support
- [ ] Blockchain integration for research verification

### Version 1.1
- [ ] Advanced search with Elasticsearch
- [ ] File versioning system
- [ ] Automated testing pipeline
- [ ] API rate limiting
- [ ] Webhook system
- [ ] Export functionality (PDF, CSV, JSON)

---

**Built with ❤️ by [070DBEK](https://github.com/070DBEK)**

*ResearchHub API - Empowering Scientific Collaboration*

