# 🌱 GreenTrack - Climatiqq

[![Django](https://img.shields.io/badge/Django-5.2.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.0.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Supabase](https://img.shields.io/badge/Supabase-8.0.0-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![SendGrid](https://img.shields.io/badge/SendGrid-6.10.0-00C88F?style=for-the-badge&logo=sendgrid&logoColor=white)](https://sendgrid.com/)

> **Track your carbon footprint, make sustainable choices, and contribute to a greener future.**

## 📖 Overview

GreenTrack - Climatiqq is a comprehensive environmental impact tracking platform that empowers users to monitor, analyze, and reduce their carbon footprint. Built with modern web technologies, it provides real-time insights into personal environmental impact across multiple metrics including carbon emissions, water usage, energy consumption, and digital footprint.

## ✨ Features

### 🌍 **Environmental Tracking**
- **Multi-metric Monitoring** - Track carbon, water, energy, and digital impact
- **Real-time Analytics** - Visualize your environmental footprint over time
- **Personalized Insights** - AI-powered suggestions for reducing impact
- **Goal Setting** - Set and track sustainability targets

### 🔐 **User Management**
- **Secure Authentication** - JWT-based user authentication system
- **Profile Management** - Comprehensive user profiles with impact statistics
- **Email Integration** - SendGrid-powered welcome emails and notifications
- **Password Recovery** - Secure token-based password reset system

### �� **Data & Analytics**
- **Impact Dashboard** - Visual representation of environmental data
- **Historical Tracking** - Monitor progress over time
- **Comparative Analysis** - Compare your impact with benchmarks
- **Export Capabilities** - Download your data for external analysis

## 🏗️ Architecture

```
greentrack-climatiqq/
├── climatiqq-backend/          # Django REST API
│   ├── tracker/                # Main Django app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API views
│   │   ├── urls.py            # URL routing
│   │   ├── serializers.py     # Data serialization
│   │   ├── tests.py           # Tests
│   │   ├── admin.py           # Admin interface
│   │   └── __init__.py        # App initialization
│   ├── sendgrid/              # SendGrid integration
│   │   ├── __init__.py        # App initialization
│   │   └── tasks.py           # Email sending tasks
│   ├── supabase/              # Supabase integration
│   │   ├── __init__.py        # App initialization
│   │   └── utils.py           # Supabase utilities
│   ├── core/                  # Core Django settings
│   │   ├── settings.py        # Main settings
│   │   ├── urls.py            # URL routing
│   │   ├── middleware.py      # Middleware
│   │   └── __init__.py        # App initialization
│   ├── static/                # Static files
│   └── requirements.txt       # Project dependencies
├── climatiqq-frontend/        # React Frontend
│   ├── src/                   # Source code
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── App.js             # Main application entry point
│   │   ├── index.js           # HTML entry point
│   │   └── __init__.js        # App initialization
│   ├── public/                # Static files
│   └── package.json           # Frontend dependencies
├── .env                       # Environment variables
├── README.md                  # This file
├── CONTRIBUTING.md           # Contributing guidelines
├── README_DEPLOYMENT.md     # Deployment instructions
└── .gitignore                 # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- SendGrid Account

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/greentrack-climatiqq.git
cd greentrack-climatiqq/climatiqq-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Frontend Setup
```bash
cd climatiqq-frontend

# Install dependencies
npm install

# Start development server
npm start
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres

# SendGrid
SENDGRID_API_KEY=SG.your_api_key_here
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Django
SECRET_KEY=your_secret_key_here
DEBUG=True
FRONTEND_URL=http://localhost:3000

# Supabase
SUPABASE_URL=https://project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/register/` - User registration
- `POST /api/login/` - User authentication
- `POST /api/logout/` - User logout
- `POST /api/change-password/` - Password change
- `POST /api/password-reset-request/` - Password reset request
- `POST /api/password-reset-confirm/` - Password reset confirmation

### User Profile Endpoints
- `GET /api/profile/` - Get user profile information
- `PUT /api/profile/` - Update user profile

### Impact Tracking Endpoints
- `GET /api/impact-entries/` - List user's impact entries
- `POST /api/impact-entries/` - Create new impact entry
- `GET /api/impact-entries/{id}/` - Get specific impact entry
- `PUT /api/impact-entries/{id}/` - Update impact entry
- `DELETE /api/impact-entries/{id}/` - Delete impact entry

## 📁 Project Structure

```
greentrack-climatiqq/
├── climatiqq-backend/          # Django REST API
│   ├── tracker/                # Main Django app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API views
│   │   ├── urls.py            # URL routing
│   │   ├── serializers.py     # Data serialization
│   │   ├── tests.py           # Tests
│   │   ├── admin.py           # Admin interface
│   │   └── __init__.py        # App initialization
│   ├── sendgrid/              # SendGrid integration
│   │   ├── __init__.py        # App initialization
│   │   └── tasks.py           # Email sending tasks
│   ├── supabase/              # Supabase integration
│   │   ├── __init__.py        # App initialization
│   │   └── utils.py           # Supabase utilities
│   ├── core/                  # Core Django settings
│   │   ├── settings.py        # Main settings
│   │   ├── urls.py            # URL routing
│   │   ├── middleware.py      # Middleware
│   │   └── __init__.py        # App initialization
│   ├── static/                # Static files
│   └── requirements.txt       # Project dependencies
├── climatiqq-frontend/        # React Frontend
│   ├── src/                   # Source code
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── App.js             # Main application entry point
│   │   ├── index.js           # HTML entry point
│   │   └── __init__.js        # App initialization
│   ├── public/                # Static files
│   └── package.json           # Frontend dependencies
├── .env                       # Environment variables
├── README.md                  # This file
├── CONTRIBUTING.md           # Contributing guidelines
├── README_DEPLOYMENT.md     # Deployment instructions
└── .gitignore                 # Git ignore rules
```

## 🧪 Testing

### Backend Testing
```bash
# Run Django tests
python manage.py test

# Test SendGrid integration
python test_sendgrid.py

# Check database connection
python manage.py dbshell
```

### API Testing
```bash
# Test with curl
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/api/profile/

# Use Postman or similar tools for comprehensive API testing
```

## 🚀 Deployment

### Supabase Database Setup
1. Create a new Supabase project
2. Execute the database schema script
3. Configure connection strings
4. Set up Row Level Security (RLS) policies

### Render Deployment
1. Connect your GitHub repository
2. Set environment variables
3. Configure build commands
4. Deploy and monitor

For detailed deployment instructions, see [README_DEPLOYMENT.md](README_DEPLOYMENT.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
