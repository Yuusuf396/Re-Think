"""
WSGI module for Render deployment.
This file allows Render to import climatiqq_backend.wsgi
"""

import os
import sys

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'climatiqq-backend')
sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django and get the application
import django
django.setup()

# Import the application from the backend config
from config.wsgi import application

# Create a wsgi module
class wsgi:
    application = application 