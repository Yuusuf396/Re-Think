# 🚀 Rethink Backend Deployment Guide

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL (recommended for production)
- Web server (nginx, Apache, etc.)
- SSL certificate
- Domain name

## 🔧 Environment Setup

### 1. Create Production Environment File

```bash
cp env.production.txt .env
```

Edit `.env` with your production values:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgres://username:password@host:port/database_name

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ Database Setup

### SQLite (Development)
```bash
python manage.py migrate
```

### PostgreSQL (Production)
```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Run migrations
python manage.py migrate
```

## 📁 Static Files

```bash
python manage.py collectstatic --noinput
```

## 🔐 Security Checklist

- [ ] `DEBUG=False`
- [ ] Strong `SECRET_KEY`
- [ ] Proper `ALLOWED_HOSTS`
- [ ] SSL certificate configured
- [ ] Database credentials secure
- [ ] CORS settings configured

## 🚀 Deployment Options

### Option 1: Heroku

1. **Install Heroku CLI**
2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
   ```

4. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   ```

### Option 2: DigitalOcean App Platform

1. **Connect your repository**
2. **Set environment variables**
3. **Configure build settings**
4. **Deploy**

### Option 3: VPS (Ubuntu/DigitalOcean)

1. **Server setup**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx postgresql
   ```

2. **Application setup**
   ```bash
   git clone your-repo
   cd your-app
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Gunicorn service**
   ```bash
   sudo nano /etc/systemd/system/rethink.service
   ```

   ```ini
   [Unit]
   Description=Rethink Django App
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/your/app
   Environment="PATH=/path/to/your/app/venv/bin"
   ExecStart=/path/to/your/app/venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. **Nginx configuration**
   ```bash
   sudo nano /etc/nginx/sites-available/rethink
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /path/to/your/app;
       }

       location / {
           include proxy_params;
           proxy_pass http://127.0.0.1:8000;
       }
   }
   ```

5. **Enable and start services**
   ```bash
   sudo systemctl enable rethink
   sudo systemctl start rethink
   sudo ln -s /etc/nginx/sites-available/rethink /etc/nginx/sites-enabled
   sudo systemctl restart nginx
   ```

## 🔍 Health Check

Test your deployment:

```bash
curl https://your-domain.com/api/v1/health/
```

Expected response:
```json
{
    "status": "healthy",
    "message": "Rethink API is running",
    "version": "1.0.0"
}
```

## 📊 Monitoring

### Logs
```bash
# Application logs
sudo journalctl -u rethink -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Performance
- Monitor CPU and memory usage
- Set up uptime monitoring
- Configure error tracking

## 🔧 Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Database connection errors**
   - Check DATABASE_URL format
   - Verify database credentials
   - Ensure database is running

3. **CORS errors**
   - Verify CORS_ALLOWED_ORIGINS
   - Check frontend domain in allowed origins

4. **500 errors**
   - Check DEBUG=False
   - Review application logs
   - Verify SECRET_KEY is set

## 🚀 Post-Deployment

1. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

2. **Test all endpoints**
   - Registration
   - Login
   - Profile
   - Entries
   - Statistics

3. **Set up monitoring**
   - Error tracking
   - Performance monitoring
   - Uptime monitoring

## 📞 Support

For deployment issues:
1. Check logs
2. Verify environment variables
3. Test locally first
4. Review security checklist

---

**🎉 Your Rethink backend is now ready for production!** 