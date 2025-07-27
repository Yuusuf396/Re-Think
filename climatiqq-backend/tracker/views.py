from django.shortcuts import render
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer
from .models import ImpactEntry
from .serializers import ImpactEntrySerializer
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
import openai
import os
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .ai_model import carbon_ai_model

# Temporarily comment out enhanced authentication views and serializers
# from .auth_views import (
#     EnhancedRegisterView, EnhancedLoginView, EnhancedPasswordChangeView,
#     EnhancedPasswordResetRequestView, EnhancedPasswordResetConfirmView,
#     UserProfileView, LogoutView, SecurityLogView
# )
# from .auth_serializers import (
#     UserRegistrationSerializer as EnhancedUserRegistrationSerializer,
#     LoginSerializer, PasswordChangeSerializer,
#     PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
#     UserProfileSerializer, SecurityLogSerializer
# )

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Simple serializer for username-only login"""
    
    def validate(self, attrs):
        # Just use standard username/password validation
        return super().validate(attrs)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        print("Registration attempt with data:", request.data)
        try:
            response = super().create(request, *args, **kwargs)
            print("User created successfully:", response.data)
            
            # Send welcome email
            if response.status_code == 201:
                user_data = response.data
                try:
                    user = User.objects.get(username=user_data['username'])
                    self.send_welcome_email(user)
                    
                    # Generate JWT tokens for the new user
                    from rest_framework_simplejwt.tokens import RefreshToken
                    refresh = RefreshToken.for_user(user)
                    
                    # Return tokens along with user data
                    response.data = {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': {
                            'username': user.username,
                            'email': user.email
                        }
                    }
                    
                except User.DoesNotExist:
                    print("User not found for welcome email")
            
            return response
        except Exception as e:
            print("Registration error:", str(e))
            raise
    
    def send_welcome_email(self, user):
        """Send welcome email to new user - DISABLED"""
        # Email functionality disabled
        print(f"📧 Welcome email DISABLED for user: {user.username}")
        return
        
        # Original email code (commented out):
        # subject = "Welcome to Rethink! 🌱"
        # message = f"""
        # Hello {user.username}!
        # 
        # Welcome to Rethink - your personal climate impact tracker!
        # 
        # 🎉 Your account has been successfully created.
        # 
        # What you can do now:
        # • Track your carbon footprint
        # • Monitor water and energy usage
        # • Get personalized AI suggestions
        # • View your environmental impact over time
        # 
        # Start your journey to a more sustainable lifestyle!
        # 
        # Best regards,
        # The Rethink Team
        # 
        # ---
        # This is an automated message. Please do not reply to this email.
        # """
        # 
        # try:
        #     send_mail(
        #         subject,
        #         message,
        #         None,  # Use DEFAULT_FROM_EMAIL from settings
        #         [user.email],
        #         fail_silently=False,
        #     )
        # except Exception as e:
        #     print(f"Failed to send welcome email: {e}")

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            return Response({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'is_active': user.is_active,
                'id': user.id
            })
        except Exception as e:
            return Response(
                {'error': 'Failed to load profile data'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        """Update user profile"""
        try:
            user = request.user
            data = request.data
            
            # Update allowed fields
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                user.email = data['email']
            
            user.save()
            
            return Response({
                'message': 'Profile updated successfully',
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'is_active': user.is_active,
                'id': user.id
            })
        except Exception as e:
            return Response(
                {'error': 'Failed to update profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImpactEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = ImpactEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ImpactEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        entry = serializer.save(user=self.request.user)
        
        # Check if this is the user's first entry
        user_entries = ImpactEntry.objects.filter(user=self.request.user)
        if user_entries.count() == 1:  # This is the first entry
            self.send_first_entry_notification(self.request.user, entry)
    
    def send_first_entry_notification(self, user, entry):
        """Send first entry notification - DISABLED"""
        # Email functionality disabled
        print(f"📧 First entry email DISABLED for user: {user.username}")
        return
        
        # Original email code (commented out):
        # subject = "🎉 Congratulations on Your First Impact Entry!"
        # message = f"""
        # Hello {user.username}!
        # 
        # 🎉 Congratulations! You've just made your first impact entry.
        # 
        # Entry Details:
        # • Type: {entry.metric_type}
        # • Value: {entry.value}
        # • Description: {entry.description}
        # • Date: {entry.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
        # 
        # This is the beginning of your sustainability journey!
        # 
        # What you can do next:
        # • Add more entries to track your progress
        # • View your impact statistics
        # • Get personalized AI suggestions
        # • Share your achievements with friends
        # 
        # Keep up the great work! 🌱
        # 
        # Best regards,
        # The Rethink Team
        # 
        # ---
        # This is an automated message. Please do not reply to this email.
        # """
        # 
        # try:
        #     send_mail(
        #         subject,
        #         message,
        #         None,  # Use DEFAULT_FROM_EMAIL from settings
        #         [user.email],
        #         fail_silently=False,
        #     )
        #     print(f"✅ First entry notification sent to {user.email}")
        # except Exception as e:
        #     print(f"❌ Failed to send first entry notification: {str(e)}")
        #     # Don't fail the entry creation if email fails
        #     pass

class ImpactEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ImpactEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ImpactEntry.objects.filter(user=self.request.user)

class ImpactStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        entries = ImpactEntry.objects.filter(user=user)
        
        # Get date range (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_entries = entries.filter(created_at__gte=thirty_days_ago)
        
        # Calculate stats
        total_entries = entries.count()
        recent_entries_count = recent_entries.count()
        
        # Sum by metric type
        metric_totals = entries.values('metric_type').annotate(
            total_value=Sum('value'),
            avg_value=Avg('value'),
            count=Count('id')
        )
        
        # Recent activity (last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_activity = entries.filter(created_at__gte=seven_days_ago).count()
        
        return Response({
            'total_entries': total_entries,
            'recent_entries': recent_entries_count,
            'recent_activity': recent_activity,
            'metric_breakdown': list(metric_totals),
        })

class AISuggestionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # Get user's recent data
        entries = ImpactEntry.objects.filter(user=user).order_by('-created_at')[:50]
        
        if not entries.exists():
            return Response({
                'suggestions': [{
                    'title': '🌱 Start Your Journey',
                    'message': 'Add your first environmental impact entry to get personalized AI suggestions!',
                    'impact': 'Low',
                    'effort': 'Low'
                }],
                'data_points_analyzed': 0
            })
        
        # Prepare data for AI model
        user_data = {
            'entries': [
                {
                    'metric_type': entry.metric_type,
                    'value': entry.value,
                    'description': entry.description,
                    'created_at': entry.created_at.isoformat()
                }
                for entry in entries
            ]
        }
        
        try:
            # Use the global AI model instance
            suggestions = carbon_ai_model.predict_suggestions(user_data)
            
            return Response({
                'suggestions': suggestions,
                'data_points_analyzed': len(entries),
                'ai_model': 'CarbonAIModel v1.0'
            })
            
        except Exception as e:
            print(f"AI suggestion error: {str(e)}")
            return Response({
                'suggestions': [{
                    'title': '🤖 AI Analysis',
                    'message': 'Our AI is analyzing your data to provide personalized suggestions. Please try again in a moment.',
                    'impact': 'Medium',
                    'effort': 'Low'
                }],
                'error': str(e)
            }, status=500)

class ChatGPTSuggestionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # Get user's recent carbon data
        entries = ImpactEntry.objects.filter(user=user).order_by('-created_at')[:20]
        
        if not entries.exists():
            return Response({
                'suggestion': "Start by adding your first carbon usage entry to get personalized suggestions!"
            })
        
        # Prepare data for ChatGPT
        carbon_data = []
        for entry in entries:
            carbon_data.append(f"{entry.metric_type}: {entry.value} ({entry.description})")
        
        user_data_summary = "\n".join(carbon_data)
        
        # Create prompt for ChatGPT
        prompt = f"""
        As a climate expert, analyze this user's carbon usage data and provide personalized suggestions to reduce their environmental impact.
        
        User's recent carbon usage:
        {user_data_summary}
        
        Please provide:
        1. A brief analysis of their current carbon footprint
        2. 3-5 specific, actionable suggestions to reduce their impact
        3. Encouraging tone with practical tips
        
        Keep the response under 300 words and make it personal and actionable.
        """
        
        try:
            # Initialize OpenAI client with new API
            client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful climate expert providing personalized carbon reduction advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            suggestion = response.choices[0].message.content
            
            return Response({
                'suggestion': suggestion,
                'data_points_analyzed': len(entries)
            })
            
        except Exception as e:
            return Response({
                'suggestion': "I'm having trouble analyzing your data right now. Please try again later or add more entries to get better suggestions.",
                'error': str(e)
            }, status=500)

# class PasswordResetRequestView(APIView):
#     permission_classes = [permissions.AllowAny]
#     
#     def post(self, request):
#         email = request.data.get('email')
#         
#         if not email:
#             return Response({'error': 'Email is required'}, status=400)
#         
#         # Basic email validation
#         if '@' not in email or '.' not in email:
#             return Response({'error': 'Please enter a valid email address'}, status=400)
#         
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             # Don't reveal if email exists or not for security
#             return Response({
#                 'message': 'If an account with this email exists, a password reset link has been sent.',
#                 'email': email
#             })
#         
#         # Generate password reset token
#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         
#         # Create reset URL
#         reset_url = f"http://localhost:3000/reset-password/{uid}/{token}"
#         
#         # Send email
#         subject = "🔐 Reset Your Rethink Password"
#         message = f"""
#         Hello {user.username}!
#         
#         You requested a password reset for your Rethink account.
#         
#         🔗 Click the link below to reset your password:
#         {reset_url}
#         
#         ⚠️  This link will expire in 24 hours for security.
#         
#         If you didn't request this password reset, please ignore this email.
#         Your account is secure and no action is needed.
#         
#         Best regards,
#         The Rethink Team 🌱
#         
#         ---
#         This is an automated message. Please do not reply to this email.
#         """
#         
#         try:
#             send_mail(
#                 subject,
#                 message,
#                 None,  # Use DEFAULT_FROM_EMAIL from settings
#                 [email],
#                 fail_silently=False,
#             )
#             return Response({
#                 'message': 'If an account with this email exists, a password reset link has been sent.',
#                 'email': email
#             })
#         except Exception as e:
#             return Response({
#                 'error': 'Failed to send email. Please try again later.',
#                 'details': str(e)
#             }, status=500)

# class PasswordResetConfirmView(APIView):
#     permission_classes = [permissions.AllowAny]
#     
#     def post(self, request):
#         uid = request.data.get('uid')
#         token = request.data.get('token')
#         new_password = request.data.get('new_password')
#         
#         if not all([uid, token, new_password]):
#             return Response({'error': 'All fields are required'}, status=400)
#         
#         try:
#             user_id = force_str(urlsafe_base64_decode(uid))
#             user = User.objects.get(pk=user_id)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return Response({'error': 'Invalid reset link'}, status=400)
#         
#         if not default_token_generator.check_token(user, token):
#             return Response({'error': 'Invalid or expired reset link'}, status=400)
#         
#         # Set new password
#         user.set_password(new_password)
#         user.save()
#         
#         return Response({'message': 'Password reset successfully'})

# class EmailVerificationView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     
#     def post(self, request):
#         user = request.user
#         
#         if user.email_verified:
#             return Response({'message': 'Email is already verified'})
#         
#         # Generate verification token
#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         
#         # Create verification URL
#         verify_url = f"http://localhost:3000/verify-email/{uid}/{token}"
#         
#         subject = "📧 Verify Your Rethink Email Address"
#         message = f"""
#         Hello {user.username}!
#         
#         Please verify your email address for your Rethink account.
#         
#         🔗 Click the link below to verify your email:
#         {verify_url}
#         
#         This link will expire in 24 hours.
#         
#         If you didn't create this account, please ignore this email.
#         
#         Best regards,
#         The Rethink Team 🌱
#         
#         ---
#         This is an automated message. Please do not reply to this email.
#         """
#         
#         try:
#             send_mail(
#                 subject,
#                 message,
#                 None,  # Use DEFAULT_FROM_EMAIL from settings
#                 [user.email],
#                 fail_silently=False,
#             )
#             return Response({'message': 'Verification email sent successfully.'})
#         except Exception as e:
#             return Response(
#                 {'error': 'Failed to send verification email.'},
#                 status=500
#             )

# class EmailVerificationConfirmView(APIView):
#     permission_classes = [permissions.AllowAny]
#     
#     def post(self, request):
#         uid = request.data.get('uid')
#         token = request.data.get('token')
#         
#         if not all([uid, token]):
#             return Response({'error': 'All fields are required'}, status=400)
#         
#         try:
#             user_id = force_str(urlsafe_base64_decode(uid))
#             user = User.objects.get(pk=user_id)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return Response({'error': 'Invalid verification link'}, status=400)
#         
#         if not default_token_generator.check_token(user, token):
#             return Response({'error': 'Invalid or expired verification link'}, status=400)
#         
#         # Mark email as verified
#         user.email_verified = True
#         user.save()
#         
#         return Response({'message': 'Email verified successfully'})

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not all([current_password, new_password]):
            return Response({'error': 'Both current and new password are required'}, status=400)
        
        # Check current password
        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, status=400)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Log security event
        self.log_password_change_event(user, request)
        
        # Send password change notification
        self.send_password_change_notification(user)
        
        return Response({'message': 'Password changed successfully'})
    
    def log_password_change_event(self, user, request):
        """Log password change event for security monitoring"""
        try:
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR', 'Unknown')
            
            # Log the event (you can extend this with a SecurityLog model)
            print(f"🔐 Security Event: Password changed for user {user.username}")
            print(f"   User ID: {user.id}")
            print(f"   IP Address: {ip_address}")
            print(f"   User Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
            print(f"   Timestamp: {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
        except Exception as e:
            print(f"❌ Failed to log password change event: {str(e)}")
    
    def send_password_change_notification(self, user):
        """Send password change notification - DISABLED"""
        # Email functionality disabled
        print(f"📧 Password change email DISABLED for user: {user.username}")
        return
        
        # Original email code (commented out):
        # from django.utils import timezone
        # 
        # # Get client IP address
        # x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip_address = x_forwarded_for.split(',')[0]
        # else:
        #     ip_address = self.request.META.get('REMOTE_ADDR', 'Unknown')
        # 
        # # Get user agent
        # user_agent = self.request.META.get('HTTP_USER_AGENT', 'Unknown')
        # 
        # subject = "🔐 Your Rethink Password Has Been Changed"
        # message = f"""
        # Hello {user.username}!
        # 
        # Your Rethink account password has been successfully changed.
        # 
        # ✅ Password change completed at: {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        # 📍 IP Address: {ip_address}
        # 🌐 User Agent: {user_agent[:100]}...
        # 
        # If you did not make this change, please:
        # 1. Contact support immediately
        # 2. Change your password again
        # 3. Enable two-factor authentication if available
        # 
        # For security reasons, we recommend:
        # • Using a strong, unique password
        # • Enabling two-factor authentication
        # • Regularly updating your password
        # • Never sharing your credentials
        # 
        # Best regards,
        # The Rethink Team 🌱
        # 
        # ---
        # This is an automated message. Please do not reply to this email.
        # """
        # 
        # try:
        #     send_mail(
        #         subject,
        #         message,
        #         None,  # Use DEFAULT_FROM_EMAIL from settings
        #         [user.email],
        #         fail_silently=False,
        #     )
        #     print(f"✅ Password change notification sent to {user.email}")
        #     print(f"   IP: {ip_address}")
        #     print(f"   Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        # except Exception as e:
        #     print(f"❌ Failed to send password change notification: {str(e)}")
        #     # Don't fail the password change if email fails
        #     pass

class TestUserView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'message': 'API is working!',
            'status': 'success',
            'timestamp': timezone.now().isoformat()
        })

# Add a simple health check endpoint
class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'message': 'Rethink API is running',
            'version': '1.0.0',
            'timestamp': timezone.now().isoformat()
        })

# Add a simple test endpoint that doesn't use auth models
class SimpleTestView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'message': 'Simple test endpoint working!',
            'status': 'success',
            'timestamp': timezone.now().isoformat()
        })
    
    def post(self, request):
        return Response({
            'message': 'POST request received!',
            'data': request.data,
            'status': 'success',
            'timestamp': timezone.now().isoformat()
        })

# Add a simple email test endpoint
# class EmailTestView(APIView):
#     permission_classes = [permissions.AllowAny]
#     
#     def post(self, request):
#         email = request.data.get('email', 'test@example.com')
#         
#         subject = "🧪 Rethink Email Test"
#         message = f"""
#         Hello!
#         
#         This is a test email from your Rethink application.
#         
#         ✅ If you receive this email, your email configuration is working!
#         
#         📧 Email backend: {settings.EMAIL_BACKEND}
#         📧 SMTP host: {settings.EMAIL_HOST}
#         📧 From: {settings.DEFAULT_FROM_EMAIL}
#         📧 Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
#         
#         Your Rethink application can now send real emails!
#         
#         Best regards,
#         Rethink Team 🌱
#         """
#         
#         try:
#             result = send_mail(
#                 subject,
#                 message,
#                 None,  # Use DEFAULT_FROM_EMAIL from settings
#                 [email],
#                 fail_silently=False,
#             )
#             
#             return Response({
#                 'message': 'Test email sent successfully!',
#                 'result': result,
#                 'email': email,
#                 'backend': settings.EMAIL_BACKEND,
#                 'smtp_host': settings.EMAIL_HOST,
#                 'from_email': settings.DEFAULT_FROM_EMAIL
#             })
#             
#         except Exception as e:
#             return Response({
#                 'error': 'Failed to send test email',
#                 'details': str(e),
#                 'backend': settings.EMAIL_BACKEND,
#                 'smtp_host': settings.EMAIL_HOST,
#                 'from_email': settings.DEFAULT_FROM_EMAIL
#             }, status=500)

@login_required
def dashboard_view(request):
    """Web view for user dashboard"""
    user = request.user
    entries = ImpactEntry.objects.filter(user=user).order_by('-created_at')[:10]  # Last 10 entries
    
    # Calculate basic stats
    total_entries = ImpactEntry.objects.filter(user=user).count()
    total_carbon = ImpactEntry.objects.filter(user=user, metric_type='carbon').aggregate(Sum('value'))['value__sum'] or 0
    
    context = {
        'user': user,
        'entries': entries,
        'total_entries': total_entries,
        'total_carbon': total_carbon,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def entries_list_view(request):
    """Web view for listing all entries"""
    entries = ImpactEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tracker/entries_list.html', {'entries': entries})

@login_required
def stats_view(request):
    """Web view for statistics"""
    user = request.user
    entries = ImpactEntry.objects.filter(user=user)
    
    # Calculate stats
    total_entries = entries.count()
    metric_breakdown = entries.values('metric_type').annotate(
        total_value=Sum('value'),
        count=Count('id')
    )
    
    context = {
        'user': user,
        'total_entries': total_entries,
        'metric_breakdown': metric_breakdown,
    }
    return render(request, 'tracker/stats.html', context)
