# 🚀 Render Deployment Guide for Rethink Backend

## 📋 Prerequisites

- GitHub repository with your code
- Render account (free tier available)
- Domain name (optional)

## 🔧 Step-by-Step Deployment

### 1. **Prepare Your Repository**

Make sure your repository has these files:
- ✅ `requirements.txt`
- ✅ `build.sh`
- ✅ `render.yaml` (optional, for automatic setup)
- ✅ `config/settings.py` (updated for production)

### 2. **Connect to Render**

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +"**
3. **Select "Web Service"**
4. **Connect your GitHub repository**

### 3. **Configure Your Service**

#### **Basic Settings:**
- **Name:** `climatiqq-backend`
- **Environment:** `Python 3`
- **Region:** Choose closest to your users
- **Branch:** `main` (or your default branch)

#### **Build & Deploy Settings:**
- **Build Command:** `chmod +x build.sh && ./build.sh`
- **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

### 4. **Environment Variables**

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

# Optional: Email settings (if you enable later)
# EMAIL_HOST=smtp.resend.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=resend
# EMAIL_HOST_PASSWORD=your-resend-api-key
```

### 5. **Add PostgreSQL Database**

1. **Go to Render Dashboard**
2. **Click "New +"**
3. **Select "PostgreSQL"**
4. **Configure:**
   - **Name:** `climatiqq-db`
   - **Database:** `climatiqq`
   - **User:** `climatiqq_user`
   - **Plan:** Free (or paid for production)

### 6. **Link Database to Web Service**

1. **Go to your web service**
2. **Click "Environment"**
3. **Add environment variable:**
   - **Key:** `DATABASE_URL`
   - **Value:** Copy from your PostgreSQL service

### 7. **Deploy**

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
   - Check `requirements.txt` syntax
   - Verify Python version compatibility
   - Check build logs for errors

2. **Database Connection Errors:**
   - Verify `DATABASE_URL` is set correctly
   - Check if PostgreSQL service is running
   - Ensure migrations ran successfully

3. **CORS Errors:**
   - Verify `CORS_ALLOWED_ORIGINS` includes your frontend URL
   - Check if frontend domain is correct

4. **500 Errors:**
   - Check `DEBUG=False`
   - Review application logs in Render dashboard
   - Verify `SECRET_KEY` is set

### **Logs:**
- **Build logs:** Available during deployment
- **Runtime logs:** In Render dashboard under your service
- **Database logs:** In PostgreSQL service dashboard

## 🔧 **Post-Deployment**

### **1. Create Superuser:**
```bash
# Use Render's shell feature
render exec climatiqq-backend python manage.py createsuperuser
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

### **Health Checks:**
- Set up external monitoring
- Configure alerts for downtime
- Monitor response times

## 🔒 **Security**

### **Production Checklist:**
- ✅ `DEBUG=False`
- ✅ Strong `SECRET_KEY`
- ✅ Proper `ALLOWED_HOSTS`
- ✅ HTTPS enabled (automatic on Render)
- ✅ Database secured
- ✅ CORS configured

## 🚀 **Scaling**

### **Free Tier Limits:**
- **Sleep after 15 minutes** of inactivity
- **512MB RAM**
- **Shared CPU**

### **Upgrade Options:**
- **Starter:** $7/month (always on, 512MB RAM)
- **Standard:** $25/month (1GB RAM, dedicated CPU)

## 📞 **Support**

### **Render Support:**
- [Render Documentation](https://render.com/docs)
- [Community Forum](https://community.render.com)
- [Status Page](https://status.render.com)

### **Common Commands:**
```bash
# View logs
render logs climatiqq-backend

# Execute commands
render exec climatiqq-backend python manage.py shell

# Restart service
render restart climatiqq-backend
```

---

**🎉 Your Rethink backend is now deployed on Render!**

**Next steps:**
1. Test all endpoints
2. Update frontend API URL
3. Set up monitoring
4. Configure custom domain (optional) 