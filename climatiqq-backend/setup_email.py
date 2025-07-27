#!/usr/bin/env python3
"""
Quick Email Setup Script for Rethink
Helps you configure real email sending
"""

import os
import sys

def setup_resend():
    """Setup Resend email service"""
    print("📧 Setting up Resend Email Service")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = '.env'
    if not os.path.exists(env_file):
        print("Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("# Email Configuration\n")
            f.write("# Get your API key from: https://resend.com\n\n")
            f.write("RESEND_API_KEY=your-resend-api-key-here\n")
            f.write("DEFAULT_FROM_EMAIL=noreply@your-domain.com\n")
    
    print("\n📧 To enable real email sending:")
    print("1. Go to https://resend.com")
    print("2. Sign up for a free account")
    print("3. Get your API key from the dashboard")
    print("4. Edit the .env file and replace 'your-resend-api-key-here' with your actual API key")
    print("5. Restart the Django server")
    
    print("\n📧 Example .env file:")
    print("RESEND_API_KEY=re_1234567890abcdef...")
    print("DEFAULT_FROM_EMAIL=noreply@yourdomain.com")
    
    print("\n✅ After setup, emails will be:")
    print("   • Printed to console (for development)")
    print("   • Sent to real email addresses")
    
    return True

def setup_gmail():
    """Setup Gmail SMTP (alternative)"""
    print("📧 Setting up Gmail SMTP")
    print("=" * 50)
    
    print("\n📧 To use Gmail SMTP:")
    print("1. Enable 2-factor authentication on your Gmail account")
    print("2. Generate an App Password: https://myaccount.google.com/apppasswords")
    print("3. Edit the .env file with your Gmail credentials")
    
    print("\n📧 Example .env file for Gmail:")
    print("EMAIL_HOST_USER=your-email@gmail.com")
    print("EMAIL_HOST_PASSWORD=your-app-password")
    print("DEFAULT_FROM_EMAIL=your-email@gmail.com")
    
    return True

def main():
    print("🚀 Rethink Email Setup")
    print("=" * 50)
    
    while True:
        print("\nChoose your email service:")
        print("1. Resend (Recommended - Free, 3,000 emails/month)")
        print("2. Gmail SMTP (Alternative)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            setup_resend()
            break
        elif choice == '2':
            setup_gmail()
            break
        elif choice == '3':
            print("Setup cancelled.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 