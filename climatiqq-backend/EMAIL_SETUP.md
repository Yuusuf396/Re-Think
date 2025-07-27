# 🌱 GreenTrack Email Setup Guide

## Current Email Features

### ✅ **Implemented Email Notifications:**

1. **Welcome Email** - Sent when user registers
2. **Password Reset Email** - Sent when user requests password reset
3. **Email Verification** - Sent when user requests email verification
4. **Password Change Notification** - Sent when user changes password
5. **First Entry Notification** - Sent when user adds their first environmental impact entry

## 🚀 Quick Setup

### **Option 1: Development Mode (Recommended for Testing)**
- Emails are printed to the console/terminal
- No external setup required
- Perfect for development and testing

### **Option 2: Gmail SMTP (For Production)**
- Uses your Gmail account to send real emails
- Requires Gmail App Password setup

## 📧 Email Setup Instructions

### **For Development (Console Backend)**
1. No setup required - emails will be printed to your terminal
2. Start your Django server and test the functionality
3. Check the terminal output for email content

### **For Production (Gmail SMTP)**

#### Step 1: Create Gmail App Password
1. Go to your Google Account settings: https://myaccount.google.com/
2. Enable 2-Step Verification if not already enabled
3. Go to Security > App passwords
4. Select "Mail" and generate a new app password
5. Copy the 16-character password

#### Step 2: Configure Credentials
Run the setup script:
```bash
cd climatiqq-backend
python setup_email.py
```

Or manually create a `.env` file:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
```

#### Step 3: Enable SMTP
Edit `config/settings.py` and uncomment the SMTP line:
```python
if DEBUG:
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

## 📬 Email Templates

### Welcome Email
- Sent to new users upon registration
- Includes app features and next steps

### Password Reset Email
- Sent when user requests password reset
- Contains secure reset link with 24-hour expiration
- Includes security warnings

### Email Verification
- Sent when user requests email verification
- Contains verification link
- Explains security benefits

### Password Change Notification
- Sent when user changes password
- Includes timestamp and security notice

### First Entry Notification
- Sent when user adds their first environmental impact entry
- Celebrates the start of their sustainability journey
- Includes entry details and encouragement

## 🔧 Testing Email Functionality

### Test Registration
1. Register a new account
2. Check terminal for welcome email

### Test Password Reset
1. Go to `/forgot-password`
2. Enter a valid email
3. Check terminal for reset email
4. Copy the reset link and test it

### Test First Entry
1. Login to an account
2. Add your first environmental impact entry
3. Check terminal for first entry notification

## 🛠️ Troubleshooting

### Common Issues:

1. **Emails not appearing in terminal**
   - Check Django server is running
   - Verify email backend is set to console
   - Check for Python errors in terminal

2. **Gmail SMTP not working**
   - Verify 2-Step Verification is enabled
   - Use App Password, not regular password
   - Check Gmail account settings

3. **Reset links not working**
   - Check URL format in terminal
   - Verify frontend is running on localhost:3000
   - Check token expiration

## 📝 Email Configuration Files

- `config/settings.py` - Email backend configuration
- `tracker/views.py` - Email sending logic
- `setup_email.py` - Interactive setup script
- `.env` - Email credentials (create this file)

## 🎯 Next Steps

1. Test all email functionality in development mode
2. Set up Gmail credentials when ready for production
3. Consider using SendGrid or Mailgun for production scale
4. Add more email notifications as needed

---

**Note:** For development, the console backend is perfect as it shows you exactly what emails would be sent without requiring external email setup. 