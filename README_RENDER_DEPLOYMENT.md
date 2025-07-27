# 🚀 Render Deployment Guide for GreenTrack

## 📋 Repository Structure

This repository has a nested structure:
```
green-track/
├── climatiqq-backend/     # Django backend
├── climatiqq-frontend/    # React frontend
├── requirements.txt       # Python dependencies (root)
├── build.sh             # Build script (root)
├── render.yaml          # Render config (root)
└── runtime.txt          # Python version (root)
```

## 🔧 Render Configuration

### **Build Command:**
```bash
chmod +x build.sh && ./build.sh
```

### **Start Command:**
```bash
cd climatiqq-backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

## 🚀 Deployment Steps

### **1. Push Changes to GitHub**
```bash
git add .
git commit -m "Add Render deployment files"
git push origin main
```

### **2. Deploy on Render**

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository: `Yuusuf396/green-track`**
4. **Configure settings:**

#### **Basic Settings:**
- **Name:** `climatiqq-backend`
- **Environment:** `Python 3`
- **Region:** Choose closest to your users
- **Branch:** `main`

#### **Build & Deploy:**
- **Build Command:** `chmod +x build.sh && ./build.sh`
- **Start Command:** `cd climatiqq-backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

### **3. Environment Variables**

Add these in Render dashboard:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=climatiqq-backend.onrender.com

# CORS Settings
CORS_ALLOWED_ORIGINS=https://climatiqq-frontend.onrender.com,http://localhost:3000

# Database (Render will provide this)
DATABASE_URL=postgres://... (auto-provided by Render)
```

### **4. Add PostgreSQL Database**

1. **Create PostgreSQL service:**
   - **Name:** `climatiqq-db`
   - **Database:** `climatiqq`
   - **User:** `climatiqq_user`
   - **Plan:** Free

2. **Link to web service:**
   - Go to your web service
   - Add environment variable `DATABASE_URL`
   - Copy value from PostgreSQL service

### **5. Deploy**

1. **Click "Create Web Service"**
2. **Wait for build to complete**
3. **Check logs for any errors**

## 🔍 **Verification**

### **Health Check:**
```bash
curl https://climatiqq-backend.onrender.com/api/v1/health/
```

Expected response:
```json
{
    "status": "healthy",
    "message": "Rethink API is running",
    "version": "1.0.0"
}
```

### **Test Endpoints:**
```bash
# Test registration
curl -X POST https://climatiqq-backend.onrender.com/api/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'

# Test login
curl -X POST https://climatiqq-backend.onrender.com/api/v1/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **Build Fails:**
   - Check if `requirements.txt` exists in root
   - Verify `build.sh` is executable
   - Check build logs for specific errors

2. **Start Command Fails:**
   - Verify `climatiqq-backend` directory exists
   - Check if `manage.py` is in the backend directory
   - Ensure `config/wsgi.py` exists

3. **Database Connection Errors:**
   - Verify `DATABASE_URL` is set correctly
   - Check if PostgreSQL service is running
   - Ensure migrations ran successfully

### **Logs:**
- **Build logs:** Available during deployment
- **Runtime logs:** In Render dashboard under your service

## 🔧 **Post-Deployment**

### **1. Create Superuser:**
```bash
# Use Render's shell feature
render exec climatiqq-backend cd climatiqq-backend && python manage.py createsuperuser
```

### **2. Test All Features:**
- ✅ Registration
- ✅ Login
- ✅ Profile management
- ✅ Impact entries
- ✅ Statistics
- ✅ AI suggestions

### **3. Update Frontend:**
Update your frontend's API base URL:
```javascript
// In your frontend config
const API_BASE_URL = 'https://climatiqq-backend.onrender.com/api/v1';
```

## 📊 **Monitoring**

### **Render Dashboard:**
- **Uptime monitoring** (built-in)
- **Performance metrics**
- **Error tracking**
- **Log access**

## 🔒 **Security**

### **Production Checklist:**
- ✅ `DEBUG=False`
- ✅ Strong `SECRET_KEY`
- ✅ Proper `ALLOWED_HOSTS`
- ✅ HTTPS enabled (automatic on Render)
- ✅ Database secured
- ✅ CORS configured

---

**🎉 Your GreenTrack backend is now ready for Render deployment!**

**Next steps:**
1. Push changes to GitHub
2. Deploy on Render
3. Test all endpoints
4. Update frontend API URL 