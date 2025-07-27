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

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

echo "✅ Build completed successfully!" 