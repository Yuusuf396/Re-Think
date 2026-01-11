# Climatiqq - Environmental Impact Tracking System

## 🎯 Project Purpose

**Climatiqq** (formerly GreenTrack) is an environmental impact tracking application that allows users to:
- Track their personal environmental impact metrics (carbon footprint, water usage, energy consumption, digital usage)
- View aggregated statistics and insights about their environmental impact
- Monitor their progress over time

The project is built with a **minimal, working-first approach** - features are implemented to enable functionality, not to showcase complexity.

---

## 📋 Development Phases

### ✅ Phase 3: Authentication (COMPLETED)
**Status**: Fully implemented and working

**Requirements Met**:
- ✅ Email + password registration
- ✅ JWT login with email + password
- ✅ Token expiry set to 24 hours
- ✅ Auth required for all trip/entry endpoints
- ❌ No password reset (intentionally excluded)
- ❌ No email verification (intentionally excluded)
- ❌ No profile editing (intentionally excluded)

**Philosophy**: "Auth exists to enable the app, not to show off."

### 🔜 Future Phases (Not Yet Implemented)
- Phase 4: Core tracking features
- Phase 5: Analytics and insights
- Phase 6: Social features (if needed)
- Phase 7: Advanced features

---

## 🏗️ Architecture Overview

### Technology Stack

**Backend**:
- **Framework**: Django 5.2.1
- **API**: Django REST Framework (DRF)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Other**: CORS headers, python-decouple for config

**Frontend**:
- **Framework**: React 18.2.0
- **Routing**: React Router DOM 6.20.1
- **Charts**: Recharts 2.8.0
- **Build**: Create React App

### Project Structure

```
Re-Think/
├── climatiqq-backend/          # Django REST API
│   ├── config/                 # Django project settings
│   │   ├── settings.py         # Main configuration (JWT, DRF, DB)
│   │   └── urls.py             # Root URL routing
│   ├── tracker/                # Main Django app
│   │   ├── models.py           # ImpactEntry model
│   │   ├── views.py            # API endpoints (auth + entries)
│   │   ├── serializers.py      # Data validation/serialization
│   │   └── urls.py             # App-level URL routing
│   └── manage.py
│
└── climatiqq-frontend/          # React frontend
    └── src/
        ├── components/          # React components
        └── services/
            └── api.js          # API client
```

---

## 📊 Data Models

### ImpactEntry Model

**Location**: `climatiqq-backend/tracker/models.py`

```python
class ImpactEntry(models.Model):
    user = ForeignKey(User)              # Links entry to user
    metric_type = CharField              # 'carbon', 'water', 'energy', 'digital'
    value = FloatField                   # Numeric impact value
    description = CharField(optional)    # User description
    created_at = DateTimeField          # Auto timestamp
```

**Purpose**: Stores individual environmental impact entries that users create.

**Relationships**:
- Many-to-One with User (one user has many entries)
- Cascade delete (if user deleted, entries deleted)

### User Model

**Location**: Django's built-in `django.contrib.auth.models.User`

**Fields Used**:
- `username` - Required, unique
- `email` - Required, unique (used for login)
- `password` - Hashed, never stored plain text

---

## 🔐 Authentication System

### JWT (JSON Web Token) Implementation

**Purpose**: Stateless authentication - server doesn't store sessions, tokens are self-contained.

**How It Works**:
1. User registers/logs in with email + password
2. Server validates credentials
3. Server generates JWT token (contains user_id, expiry, signature)
4. Client stores token (localStorage)
5. Client sends token in `Authorization: Bearer <token>` header
6. Server validates token on each request
7. If valid, sets `request.user` automatically

### Token Configuration

**Location**: `climatiqq-backend/config/settings.py`

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),  # Token valid for 24 hours
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),   # Refresh token valid 1 day
    'ALGORITHM': 'HS256',                          # Signing algorithm
    'SIGNING_KEY': SECRET_KEY,                      # Secret key for signing
    'AUTH_HEADER_TYPES': ('Bearer',),              # Header format
}
```

### Authentication Endpoints

#### 1. Registration: `POST /api/v1/register/`

**Request**:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "password123",
  "password_confirm": "password123"
}
```

**Response** (201 Created):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "username": "johndoe",
    "email": "john@example.com"
  },
  "message": "User registered successfully"
}
```

**What Happens**:
1. Validates passwords match
2. Checks username/email uniqueness
3. Creates user with hashed password
4. Generates JWT tokens
5. Returns tokens + user info

**Code**: `tracker/views.py` → `RegisterView`

#### 2. Login: `POST /api/v1/login/`

**Request**:
```json
{
  "username": "john@example.com",  # Actually email, field named 'username'
  "password": "password123"
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**What Happens**:
1. Accepts email (custom serializer converts field)
2. Looks up user by email
3. Validates password
4. Generates JWT tokens
5. Returns tokens

**Code**: `tracker/views.py` → `CustomTokenObtainPairView` + `CustomTokenObtainPairSerializer`

**Key Implementation Detail**: The serializer overrides the `username` field to accept email addresses, then converts it back to username for token generation.

---

## 🛣️ API Endpoints

### Base URL: `/api/v1/`

### Public Endpoints (No Auth Required)

| Method | Endpoint | Purpose | View Class |
|--------|----------|---------|------------|
| POST | `/register/` | User registration | `RegisterView` |
| POST | `/login/` | User login | `CustomTokenObtainPairView` |
| POST | `/logout/` | Logout (placeholder) | `LogoutView` |

### Protected Endpoints (JWT Auth Required)

| Method | Endpoint | Purpose | View Class |
|--------|----------|---------|------------|
| GET | `/entries/` | List user's impact entries | `ImpactEntryListCreateView` |
| POST | `/entries/` | Create new impact entry | `ImpactEntryListCreateView` |
| GET | `/entries/<id>/` | Get specific entry | `ImpactEntryDetailView` |
| PUT | `/entries/<id>/` | Update entry | `ImpactEntryDetailView` |
| DELETE | `/entries/<id>/` | Delete entry | `ImpactEntryDetailView` |
| GET | `/stats/` | Get aggregated statistics | `ImpactStatsView` |

### Authentication Header Format

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

### Example Protected Request

```http
GET /api/v1/entries/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**What Happens**:
1. DRF middleware extracts token from header
2. Validates token signature and expiry
3. Extracts `user_id` from token payload
4. Sets `request.user` to User object
5. View checks `IsAuthenticated` permission → passes
6. View filters queryset to `user=self.request.user`
7. Returns only that user's entries

---

## 🔄 Request Flow Examples

### Example 1: User Creates Impact Entry

```
1. User fills form: {metric_type: "carbon", value: 5.2, description: "Drove to work"}
2. Frontend sends: POST /api/v1/entries/ + Authorization header
3. Backend validates JWT token
4. Backend sets request.user = authenticated user
5. ImpactEntryListCreateView.perform_create() runs
6. serializer.save(user=self.request.user) - automatically attaches user
7. Entry saved to database
8. Response: {id: 1, metric_type: "carbon", value: 5.2, ...}
```

### Example 2: User Views Their Stats

```
1. Frontend sends: GET /api/v1/stats/ + Authorization header
2. Backend validates JWT token
3. ImpactStatsView.get() runs
4. Queryset filtered: ImpactEntry.objects.filter(user=request.user)
5. Aggregations calculated (totals, averages, counts)
6. Response: {total_entries: 10, recent_entries: 5, ...}
```

---

## 🔒 Security Features

### Implemented

1. **Password Hashing**: Django automatically hashes passwords (bcrypt/PBKDF2)
2. **JWT Signing**: Tokens signed with SECRET_KEY, tamper-resistant
3. **Token Expiry**: Access tokens expire after 24 hours
4. **User Isolation**: Users can only access their own entries via queryset filtering
5. **CORS Configuration**: Configured for frontend communication

### Not Implemented (By Design)

- Password reset functionality
- Email verification
- Profile editing
- Token refresh endpoint (refresh token exists but no endpoint yet)
- Rate limiting
- Token blacklisting (configured but not actively used)

---

## 📁 Key Files Explained

### Backend Files

#### `config/settings.py`
- **Purpose**: Django project configuration
- **Key Sections**:
  - `REST_FRAMEWORK`: Sets JWT as default auth, requires auth by default
  - `SIMPLE_JWT`: JWT token configuration (24h expiry, HS256 algorithm)
  - `DATABASES`: PostgreSQL/SQLite configuration
  - `CORS_ALLOW_ALL_ORIGINS`: Allows frontend to make requests

#### `tracker/models.py`
- **Purpose**: Database models
- **Models**: `ImpactEntry` - stores user's environmental impact data

#### `tracker/serializers.py`
- **Purpose**: Data validation and serialization
- **Serializers**:
  - `UserRegistrationSerializer`: Validates registration data, creates user
  - `ImpactEntrySerializer`: Validates entry data, handles creation

#### `tracker/views.py`
- **Purpose**: API endpoint logic
- **Views**:
  - `RegisterView`: Handles user registration
  - `CustomTokenObtainPairView`: Handles login
  - `CustomTokenObtainPairSerializer`: Custom login serializer (email-based)
  - `ImpactEntryListCreateView`: List/create entries
  - `ImpactEntryDetailView`: Get/update/delete entry
  - `ImpactStatsView`: Get aggregated statistics

#### `tracker/urls.py`
- **Purpose**: URL routing for tracker app
- **Routes**: Maps URLs to views (register, login, entries, stats)

#### `config/urls.py`
- **Purpose**: Root URL configuration
- **Routes**: Includes tracker URLs at `/api/v1/`

### Frontend Files

#### `src/services/api.js`
- **Purpose**: API client for making HTTP requests
- **Methods**: `auth.register()`, `auth.login()`, `entries.getAll()`, etc.

#### `src/components/`
- **Purpose**: React UI components
- **Components**: Login, Register, Dashboard, Header

---

## 🔗 How Everything Connects

### Registration Flow
```
User → Frontend Form → api.js → POST /api/v1/register/
→ RegisterView → UserRegistrationSerializer → User.objects.create_user()
→ RefreshToken.for_user() → JWT tokens generated
→ Response with tokens → Frontend stores in localStorage
```

### Login Flow
```
User → Frontend Form → api.js → POST /api/v1/login/
→ CustomTokenObtainPairView → CustomTokenObtainPairSerializer
→ User.objects.get(email=email) → user.check_password()
→ TokenObtainPairSerializer.validate() → JWT tokens generated
→ Response with tokens → Frontend stores in localStorage
```

### Protected Request Flow
```
Frontend → api.js (adds Authorization header) → GET /api/v1/entries/
→ DRF Middleware → JWTAuthentication.authenticate()
→ Token validated → request.user set
→ ImpactEntryListCreateView → permission_classes check
→ get_queryset() filters by user → Returns user's entries
```

---

## 🎯 Current Status

### ✅ Completed
- User registration with email + password
- JWT login with email + password
- Token-based authentication
- Protected endpoints (entries, stats)
- User data isolation (users only see their own data)
- Basic CRUD for impact entries
- Statistics aggregation

### 🔜 Next Steps (Future Phases)
- Enhanced analytics and visualizations
- Trip/activity categorization
- Historical trends
- Goal setting and tracking
- Export functionality
- Mobile responsiveness improvements

---

## 🧪 Testing the System

### Registration Test
```bash
curl -X POST http://localhost:8000/api/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "password_confirm": "password123"
  }'
```

### Login Test
```bash
curl -X POST http://localhost:8000/api/v1/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test@example.com",
    "password": "password123"
  }'
```

### Protected Endpoint Test
```bash
curl -X GET http://localhost:8000/api/v1/entries/ \
  -H "Authorization: Bearer <access_token_from_login>"
```

---

## 📝 Important Notes for AI Assistants

1. **Minimal Approach**: This project prioritizes working functionality over feature completeness. Don't add unnecessary complexity.

2. **Authentication**: All trip/entry endpoints require JWT authentication. The token must be sent in the `Authorization: Bearer <token>` header.

3. **User Isolation**: Always filter querysets by `user=self.request.user` to ensure users only see their own data.

4. **Email Login**: Login uses email addresses, but the field is named `username` in the API request (due to JWT serializer requirements).

5. **Token Lifetime**: Access tokens expire after 24 hours. Users need to log in again after expiry.

6. **No Password Reset**: This is intentional - not a missing feature.

7. **Database**: Uses PostgreSQL in production, SQLite in development (auto-detected via environment variables).

8. **CORS**: Configured to allow all origins in development. Should be restricted in production.

---

## 🚀 Quick Start

### Backend
```bash
cd climatiqq-backend
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd climatiqq-frontend
npm install
npm start
```

---

## 📚 Key Concepts Summary

- **JWT**: Stateless authentication tokens that contain user identity
- **Serializer**: Validates and transforms data between API and database
- **View**: Handles HTTP requests and returns responses
- **Queryset Filtering**: Ensures users only access their own data
- **Permission Classes**: Control who can access endpoints
- **Token Expiry**: Security measure - tokens expire after set time

---

**Last Updated**: Phase 3 (Authentication) Complete
**Next Phase**: Core tracking features and enhancements

