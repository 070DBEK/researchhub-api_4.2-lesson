@echo off
echo 🔧 Fixing ResearchHub API migrations...

echo 📊 Checking current migration status...
python manage.py showmigrations

echo 🗑️ Removing old migration files...
for /d %%i in (apps\*) do (
    if exist "%%i\migrations" (
        echo Cleaning %%i migrations...
        del /q "%%i\migrations\*.py" 2>nul
        echo. > "%%i\migrations\__init__.py"
    )
)

echo 📝 Creating fresh migrations...
python manage.py makemigrations users
python manage.py makemigrations profiles
python manage.py makemigrations research_groups
python manage.py makemigrations projects
python manage.py makemigrations experiments
python manage.py makemigrations findings
python manage.py makemigrations attachments
python manage.py makemigrations publications
python manage.py makemigrations comments
python manage.py makemigrations likes
python manage.py makemigrations messages
python manage.py makemigrations notifications
python manage.py makemigrations analytics
python manage.py makemigrations tags

echo 🗄️ Applying all migrations...
python manage.py migrate

echo ✅ Migrations fixed!
echo 👤 Creating superuser...
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
    print('ℹ️ Superuser already exists')
"

echo 🎉 Setup complete! You can now run: python manage.py runserver
pause
