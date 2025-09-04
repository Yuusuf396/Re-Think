#!/bin/bash

echo "🚀 Starting Climatiqq Backend with Supabase..."

# Run migrations
echo "📦 Running database migrations..."
python manage.py migrate

# Create superuser if none exists
echo "👑 Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@climatiqq.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Start the server
echo "🌐 Starting Django server..."
python manage.py runserver 0.0.0.0:8000
