# SendGrid Integration Setup Guide

This guide will help you set up SendGrid email integration for your GreenTrack - Climatiqq Django application.

## 🚀 Quick Start

### 1. Get SendGrid API Key

1. Go to [SendGrid.com](https://sendgrid.com) and create an account
2. Navigate to **Settings → API Keys**
3. Click **Create API Key**
4. Choose **Full Access** or **Restricted Access** with Mail Send permissions
5. Copy your API key (starts with `SG.`)

### 2. Configure Environment Variables

Copy the sample environment file and update it with your values:

```bash
cp env.sample .env
```

Edit `.env` and update these values:

```env
# SendGrid Configuration
SENDGRID_API_KEY=SG.your_actual_api_key_here
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
SUPPORT_EMAIL=support@yourdomain.com
FRONTEND_URL=http://localhost:3000

# Email Backend
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### 3. Verify Domain (Optional but Recommended)

For production use, verify your domain in SendGrid:

1. Go to **Settings → Sender Authentication**
2. Choose **Domain Authentication**
3. Follow the DNS setup instructions
4. Wait for verification (can take up to 24 hours)

## 📧 Email Features

### Registration Welcome Email
- **Trigger**: When a user registers
- **Template**: `templates/emails/registration_welcome.html`
- **Endpoint**: `POST /api/register/`

### Password Reset Email
- **Trigger**: When user requests password reset
- **Template**: `templates/emails/password_reset.html`
- **Endpoint**: `POST /api/password-reset-request/`

### Password Change Confirmation
- **Trigger**: When password is changed
- **Template**: `templates/emails/password_changed.html`
- **Endpoint**: `POST /api/change-password/`

## 🔧 API Endpoints

### Password Reset Flow

1. **Request Password Reset**
   ```http
   POST /api/password-reset-request/
   Content-Type: application/json
   
   {
     "email": "user@example.com"
   }
   ```

2. **Confirm Password Reset**
   ```http
   POST /api/password-reset-confirm/
   Content-Type: application/json
   
   {
     "uid": "base64_encoded_user_id",
     "token": "reset_token",
     "new_password": "new_password123"
   }
   ```

### Response Format

All email endpoints return consistent response format:

```json
{
  "message": "Email sent successfully",
  "email_sent": true,
  "email_status": 202,
  "message_id": "abc123.def456.ghi789"
}
```

## 🧪 Testing

### Run the Test Suite

```bash
python test_sendgrid.py
```

This will test:
- ✅ Configuration validation
- ✅ Service initialization
- ✅ Template rendering
- ✅ SendGrid connection (optional)

### Manual Testing

1. **Test Registration Email**
   ```bash
   # Register a new user via API
   curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
   ```

2. **Test Password Reset**
   ```bash
   # Request password reset
   curl -X POST http://localhost:8000/api/password-reset-request/ \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com"}'
   ```

## 🔍 Troubleshooting

### Common Issues

1. **"SendGrid not configured" error**
   - Check if `SENDGRID_API_KEY` is set in `.env`
   - Verify the API key is correct

2. **"Failed to send email" error**
   - Check SendGrid dashboard for delivery status
   - Verify sender email is verified
   - Check API key permissions

3. **Templates not found**
   - Ensure email templates are in `tracker/templates/emails/`
   - Check template file names match the service calls

### Debug Mode

Enable debug logging in Django settings:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'tracker.services.sendgrid_service': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📊 Monitoring

### SendGrid Dashboard
- Monitor email delivery rates
- Track bounces and spam reports
- View analytics and engagement metrics

### Django Logs
- Email sending status
- Error messages and stack traces
- API response codes

## 🚀 Production Deployment

### Environment Variables
```env
SENDGRID_API_KEY=SG.production_api_key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
SUPPORT_EMAIL=support@yourdomain.com
FRONTEND_URL=https://yourdomain.com
```

### Security Considerations
- Never commit API keys to version control
- Use environment variables for sensitive data
- Enable domain authentication in SendGrid
- Monitor for suspicious activity

### Performance
- SendGrid handles up to 100 emails per second on free tier
- Paid plans support higher throughput
- Consider rate limiting for bulk operations

## 📚 Additional Resources

- [SendGrid API Documentation](https://sendgrid.com/docs/api-reference/)
- [Django Email Documentation](https://docs.djangoproject.com/en/stable/topics/email/)
- [SendGrid Best Practices](https://sendgrid.com/docs/ui/sending-email/deliverability/)

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run the test suite: `python test_sendgrid.py`
3. Check SendGrid dashboard for delivery status
4. Review Django logs for error messages
5. Verify all environment variables are set correctly

---

**Happy Email Sending! 🎉**
