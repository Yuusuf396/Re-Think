"""
WSGI config for the project.
Redirects to the backend Django application.
"""

import os
import sys

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'climatiqq-backend')
sys.path.insert(0, backend_path)

# Change to the backend directory
os.chdir(backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django and get the application
import django
django.setup()

from config.wsgi import application 