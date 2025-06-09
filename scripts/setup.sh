#!/bin/bash

echo "🚀 Setting up ResearchHub API..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Determine environment
ENVIRONMENT=${DJANGO_ENVIRONMENT:-development}
echo "🌍 Environment: $ENVIRONMENT"

# Install dependencies based on environment
if [ "$ENVIRONMENT" = "production" ]; then
    echo "📚 Installing production dependencies..."
    pip install -r requirements/production.txt
else
    echo "📚 Installing development dependencies..."
    pip install -r requirements/development.txt
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env-example.txt .env
    echo "⚠️  Please update .env file with your settings"
fi

# Create logs directory
mkdir -p logs

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@researchhub.com').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@researchhub.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✅ Superuser created: admin@researchhub.com / admin123')
else:
    print('ℹ️  Superuser already exists')
"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup complete!"
echo ""
echo "🌐 Available endpoints:"
echo "   - API Documentation: http://localhost:8000/api/docs/"
echo "   - Admin Panel: http://localhost:8000/admin/"
echo "   - API Root: http://localhost:8000/api/v1/"
echo ""
echo "🚀 To start the server:"
echo "   python manage.py runserver"
echo ""
echo "🧪 To run tests:"
echo "   python manage.py test"
echo ""
echo "📊 To check code quality:"
echo "   black . && flake8 . && isort ."
