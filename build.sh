#!/usr/bin/env bash
# Build script for Render deployment

echo "🚀 Starting build process..."

# Install Python dependencies (from root directory)
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Change to backend directory
cd climatiqq-backend

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Check migration status
echo "📊 Checking migration status..."
python manage.py showmigrations

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --verbosity=2

# Check migration status again
echo "📊 Final migration status..."
python manage.py showmigrations

# Create test user
echo "👤 Creating test user..."
python create_test_user.py

# Create superuser if needed (optional)
echo "👤 Checking if superuser exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print('Creating admin user...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created!')
else:
    print('Admin user already exists')
"

echo "✅ Build completed successfully!" 