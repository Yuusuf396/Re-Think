# 📧 Email Setup Guide for Rethink

## 🚀 Quick Setup (Development)

For development, emails are automatically sent to the console (terminal). No setup required!

## 📧 Production Email Setup

### Option 1: Gmail SMTP (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Create `.env` file** in `climatiqq-backend/`:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-digit-app-password
   ```

### Option 2: Other Email Providers

#### Outlook/Hotmail
```
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### Yahoo
```
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### Custom SMTP
```
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@domain.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 🔧 Configuration

### Development (Console)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production (SMTP)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

## 📬 Email Features

### 1. Welcome Email
- **Trigger**: User registration
- **Content**: Welcome message, app features, getting started guide

### 2. Password Reset
- **Trigger**: User requests password reset
- **Content**: Reset link with token, security notes

### 3. Email Verification
- **Trigger**: User requests email verification
- **Content**: Verification link, benefits of verified account

### 4. Password Change Notification
- **Trigger**: User changes password
- **Content**: Confirmation, timestamp, security tips

### 5. First Entry Notification
- **Trigger**: User adds first environmental entry
- **Content**: Congratulations, encouragement, next steps

## 🛠️ Testing Email Setup

### 1. Test SMTP Connection
```bash
cd climatiqq-backend
python manage.py shell
```

```python
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email from Rethink!',
    None,  # Uses DEFAULT_FROM_EMAIL
    ['your-email@gmail.com'],
    fail_silently=False,
)
```

### 2. Test Password Reset
1. Go to `/forgot-password`
2. Enter your email
3. Check console/email for reset link

### 3. Test Email Verification
1. Login to your account
2. Go to Profile → Email Verification
3. Check console/email for verification link

## 🔒 Security Best Practices

1. **Use App Passwords** (not regular passwords)
2. **Environment Variables** (never hardcode credentials)
3. **TLS Encryption** (always use TLS)
4. **Rate Limiting** (prevent abuse)
5. **Email Validation** (verify email format)

## 🚨 Troubleshooting

### Common Issues:

1. **"Authentication failed"**
   - Check app password is correct
   - Ensure 2FA is enabled

2. **"Connection refused"**
   - Check firewall settings
   - Verify SMTP host/port

3. **"Invalid credentials"**
   - Regenerate app password
   - Check email address format

4. **"TLS required"**
   - Ensure `EMAIL_USE_TLS = True`
   - Check port 587 (not 465)

### Debug Mode:
```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 📱 Frontend Integration

The frontend automatically handles:
- ✅ Password reset forms
- ✅ Email verification requests
- ✅ Success/error messages
- ✅ Loading states

## 🎯 Next Steps

1. **Set up Gmail SMTP** (recommended)
2. **Test all email features**
3. **Deploy to production**
4. **Monitor email delivery**

---

**Need help?** Check the Django documentation or contact support! 