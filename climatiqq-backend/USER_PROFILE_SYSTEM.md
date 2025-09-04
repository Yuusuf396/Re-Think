# 🚀 User Profile System Documentation

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Authentication & Security](#authentication--security)
- [Email Integration](#email-integration)
- [Setup & Configuration](#setup--configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## Overview

The User Profile System is a comprehensive feature that provides authenticated users with access to their personal information, statistics, and account details. This system integrates seamlessly with the existing SendGrid email service and Supabase PostgreSQL database infrastructure.

### **System Architecture**
```
Frontend (React) → Django REST API → PostgreSQL Database
                     ↓
              SendGrid Email Service
```

## ✨ Features

### **Core Profile Features**
- 🔐 **Secure Authentication** - JWT-based access control
- **User Information Display** - Username, email, names, join date
- 📊 **Impact Statistics** - Count of user's carbon impact entries
- 🕒 **Activity Tracking** - Last login timestamp
- 🔄 **Real-time Updates** - Live data from database

### **Email Integration Features**
- **Welcome Emails** - Sent upon successful registration
- **Password Reset** - Secure token-based password recovery
- ✅ **Password Change Confirmation** - Email notifications for security
- 🎨 **Professional Templates** - HTML and plain text email formats

## API Endpoints

### **User Profile Endpoint**

#### **GET /api/profile/**
Retrieves authenticated user's profile information.

**Headers Required:**
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Response Format:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2024-01-15",
    "impact_entries_count": 12,
    "is_active": true,
    "last_login": "2024-01-15 14:30"
}
```

**HTTP Status Codes:**
- `200 OK` - Profile data retrieved successfully
- `401 Unauthorized` - Invalid or missing JWT token
- `403 Forbidden` - User account is inactive

### **Authentication Endpoints**

#### **POST /api/register/**
User registration with automatic welcome email.

#### **POST /api/login/**
User authentication with JWT token generation.

#### **POST /api/change-password/**
Password change with confirmation email.

#### **POST /api/password-reset-request/**
Password reset request via email.

#### **POST /api/password-reset-confirm/**
Password reset confirmation with token.

##️ Database Models

### **User Model (Django Built-in)**
```python
class User(AbstractUser):
    # Inherits from Django's AbstractUser
    # username, email, first_name, last_name
    # date_joined, last_login, is_active
    # password, groups, permissions
```

### **ImpactEntry Model**
```python
class ImpactEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=20, choices=METRIC_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **Database Schema (PostgreSQL)**
```sql
-- User profiles table
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    date_joined TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Impact entries table
CREATE TABLE impact_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user_profiles(id),
    metric_type VARCHAR(20) NOT NULL,
    value DECIMAL(10, 4) NOT NULL,
    description VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🔐 Authentication & Security

### **JWT Token System**
- **Access Token** - Short-lived (15 minutes) for API requests
- **Refresh Token** - Long-lived (7 days) for token renewal
- **Automatic Refresh** - Seamless token management

### **Security Features**
- **Row Level Security (RLS)** - Database-level access control
- **CORS Configuration** - Cross-origin request handling
- **Rate Limiting** - API abuse prevention
- **Input Validation** - XSS and injection protection

### **Permission Classes**
```python
from rest_framework.permissions import IsAuthenticated, AllowAny

# Public endpoints (registration, login)
permission_classes = [AllowAny]

# Protected endpoints (profile, password change)
permission_classes = [IsAuthenticated]
```

## 📧 Email Integration

### **SendGrid Service**
```python
class SendGridService:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.app_name = settings.APP_NAME
        self.frontend_url = settings.FRONTEND_URL
    
    def send_registration_email(self, user, request):
        # Welcome email with app introduction
    
    def send_password_reset_email(self, user, request):
        # Reset link with secure token
    
    def send_password_change_confirmation(self, user):
        # Security confirmation email
```

### **Email Templates**
- **HTML Format** - Rich, responsive design
- **Plain Text** - Fallback for email clients
- **Dynamic Content** - Personalized user information
- **Brand Consistency** - App name, colors, and styling

### **Email Types**
1. **Welcome Email** - Sent after successful registration
2. **Password Reset** - Secure token-based recovery
3. **Password Change** - Security confirmation
4. **Account Verification** - Future enhancement

## ⚙️ Setup & Configuration

### **Environment Variables (.env)**
```env
# Supabase PostgreSQL
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres

# SendGrid Configuration
SENDGRID_API_KEY=SG.your_api_key_here
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
SUPPORT_EMAIL=support@yourdomain.com

# Django Settings
SECRET_KEY=your_secret_key_here
DEBUG=True
FRONTEND_URL=http://localhost:3000

# Supabase Additional
SUPABASE_URL=https://project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### **Django Settings Configuration**
```python
# settings.py

# Database Configuration
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL and DATABASE_URL.startswith('postgres'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }

# SendGrid Email Configuration
SENDGRID_API_KEY = config('SENDGRID_API_KEY')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# User Profile Configuration
USER_PROFILE_ENABLED = True
USER_PROFILE_DETAILS = [
    'username', 'email', 'first_name', 'last_name', 
    'date_joined', 'impact_count'
]
```

### **Dependencies (requirements.txt)**
```
Django==5.2.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
sendgrid==6.10.0
psycopg2-binary==2.9.7
dj-database-url==2.1.0
python-decouple==3.8
```

## 🧪 Testing

### **Manual Testing**
```bash
# Start Django server
python manage.py runserver

# Test profile endpoint
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/api/profile/
```

### **SendGrid Testing**
```bash
# Run SendGrid test script
python test_sendgrid.py

# Test email templates
python -c "
from django.template.loader import render_to_string
from django.conf import settings
context = {'user': {'username': 'test'}, 'app_name': 'Test App'}
print(render_to_string('emails/registration_welcome.html', context))
"
```

### **Database Testing**
```bash
# Test PostgreSQL connection
python manage.py dbshell

# Run migrations
python manage.py migrate

# Check database status
python manage.py showmigrations
```

## Deployment

### **Supabase Setup**
1. Create Supabase project
2. Execute database schema script
3. Configure environment variables
4. Test database connection

### **Render Deployment**
1. Connect GitHub repository
2. Set environment variables
3. Deploy Django application
4. Monitor application logs

### **Environment Configuration**
```bash
# Production settings
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 🔧 Troubleshooting

### **Common Issues**

#### **Database Connection Errors**
```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Test connection manually
psql "postgresql://postgres:password@db.project.supabase.co:5432/postgres"
```

#### **SendGrid Email Failures**
```bash
# Verify API key
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.sendgrid.com/v3/user/profile

# Check sender verification
# Ensure DEFAULT_FROM_EMAIL is verified in SendGrid
```

#### **JWT Token Issues**
```bash
# Check token expiration
python manage.py shell
from rest_framework_simplejwt.tokens import AccessToken
token = AccessToken()
print(token.lifetime)
```

### **Debug Commands**
```bash
# Check Django settings
python manage.py check

# Verify database
python manage.py dbshell

# Test email configuration
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### **Log Files**
```bash
# Django logs
tail -f logs/django.log

# Application logs
tail -f logs/app.log

# Error logs
tail -f logs/error.log
```

## 📚 Additional Resources

### **Documentation Links**
- [Django REST Framework](https://www.django-rest-framework.org/)
- [SendGrid API Documentation](https://sendgrid.com/docs/api-reference/)
- [Supabase Documentation](https://supabase.com/docs)
- [JWT Token Guide](https://django-rest-framework-simplejwt.readthedocs.io/)

### **Code Examples**
- [Complete API Implementation](tracker/views.py)
- [URL Configuration](tracker/urls.py)
- [Email Templates](tracker/templates/emails/)
- [Database Models](tracker/models.py)

### **Testing Tools**
- [Postman](https://www.postman.com/) - API testing
- [pgAdmin](https://www.pgadmin.org/) - PostgreSQL management
- [SendGrid Dashboard](https://app.sendgrid.com/) - Email analytics

## 🎉 Conclusion

The User Profile System provides a robust foundation for user management, authentication, and communication. With integrated email services, secure authentication, and scalable database architecture, this system is ready for production deployment and future enhancements.

### **Next Steps**
1. **Deploy to production** using the provided configuration
2. **Monitor performance** and user engagement
3. **Add analytics** for user behavior tracking
4. **Implement caching** for improved response times
5. **Add user preferences** and customization options

---

**Last Updated:** January 2024  
**Version:** 1.0.0  
**Maintainer:** Development Team  
**Support:** support@climatiqq.com
```

**Perfect! I've created the comprehensive markdown documentation file in your `climatiqq-backend` folder!** 📚✨

The file `USER_PROFILE_SYSTEM.md` is now located at:
```
<code_block_to_apply_changes_from>
```

This documentation covers your entire user profile system including:
- ✅ Complete system overview and architecture
- ✅ API endpoints and usage examples
- ✅ Database models and PostgreSQL schema
- ✅ Authentication and security features
- ✅ SendGrid email integration
- ✅ Setup and configuration steps
- ✅ Testing procedures
- ✅ Deployment instructions
- ✅ Troubleshooting guide

Now you can commit this documentation along with your code changes! 🚀