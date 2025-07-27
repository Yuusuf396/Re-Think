"""
Custom email backend that both prints to console and sends via SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
import os

class ConsoleAndSMTPBackend(BaseEmailBackend):
    """
    Custom email backend that:
    1. Prints emails to console (for development visibility)
    2. Sends emails via SMTP (for real delivery)
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console_backend = None
        self.smtp_backend = None
        
        # Initialize console backend for printing
        from django.core.mail.backends.console import EmailBackend as ConsoleBackend
        self.console_backend = ConsoleBackend()
        
        # Initialize SMTP backend for real sending
        from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
        self.smtp_backend = SMTPBackend()
    
    def send_messages(self, email_messages):
        """Send messages via both console and SMTP"""
        results = []
        
        for message in email_messages:
            # 1. Print to console (always)
            try:
                print("\n" + "="*60)
                print("📧 EMAIL SENT (Console Output)")
                print("="*60)
                print(f"From: {message.from_email}")
                print(f"To: {', '.join(message.to)}")
                print(f"Subject: {message.subject}")
                print(f"Date: {message.date}")
                print("-"*60)
                print("Content:")
                print(message.body)
                print("="*60)
                print("✅ Email printed to console successfully")
            except Exception as e:
                print(f"❌ Failed to print email to console: {e}")
            
            # 2. Send via SMTP (if configured)
            try:
                # Check if SMTP is properly configured
                if (self.smtp_backend and 
                    hasattr(settings, 'EMAIL_HOST_PASSWORD') and 
                    settings.EMAIL_HOST_PASSWORD):
                    
                    smtp_result = self.smtp_backend.send_messages([message])
                    if smtp_result:
                        print(f"✅ Email sent via SMTP to: {', '.join(message.to)}")
                    else:
                        print(f"❌ Failed to send email via SMTP to: {', '.join(message.to)}")
                else:
                    print("⚠️ SMTP not configured - email only printed to console")
                    print("   To enable real email sending, set RESEND_API_KEY in .env file")
            except Exception as e:
                print(f"❌ SMTP sending failed: {e}")
                print("📧 Email was still printed to console above")
            
            results.append(1)  # Count as sent if printed to console
        
        return len(results)
    
    def open(self):
        """Open connection to SMTP server"""
        if self.smtp_backend:
            return self.smtp_backend.open()
        return None
    
    def close(self):
        """Close connection to SMTP server"""
        if self.smtp_backend:
            return self.smtp_backend.close()
        return None 