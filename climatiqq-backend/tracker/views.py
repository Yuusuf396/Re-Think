from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
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

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        print("Registration attempt with data:", request.data)
        try:
            response = super().create(request, *args, **kwargs)
            print("User created successfully:", response.data)
            return response
        except Exception as e:
            print("Registration error:", str(e))
            raise

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        # Simple email to username conversion
        username_or_email = request.data.get('username', '')
        
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                # Create a new request data with username
                request.data = request.data.copy()
                request.data['username'] = user.username
            except User.DoesNotExist:
                pass  # Let the parent class handle the error
        
        return super().post(request, *args, **kwargs)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })

class ImpactEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = ImpactEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ImpactEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return Response({'error': 'Please enter a valid email address'}, status=400)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            return Response({
                'message': 'If an account with this email exists, a password reset link has been sent.',
                'email': email
            })
        
        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create reset URL
        reset_url = f"http://localhost:3000/reset-password/{uid}/{token}"
        
        # Send email
        subject = "Reset Your GreenTrack Password"
        message = f"""
        Hello {user.username},
        
        You requested a password reset for your GreenTrack account.
        
        Click the link below to reset your password:
        {reset_url}
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        The GreenTrack Team
        """
        
        try:
            send_mail(
                subject,
                message,
                'noreply@greentrack.com',
                [email],
                fail_silently=False,
            )
            return Response({
                'message': 'If an account with this email exists, a password reset link has been sent.',
                'email': email
            })
        except Exception as e:
            return Response({
                'error': 'Failed to send email. Please try again later.',
                'details': str(e)
            }, status=500)

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not all([uid, token, new_password]):
            return Response({'error': 'All fields are required'}, status=400)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid reset link'}, status=400)
        
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired reset link'}, status=400)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password reset successfully'})

class EmailVerificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        # Generate verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Create verification URL
        verify_url = f"http://localhost:3000/verify-email/{uid}/{token}"
        
        # Send verification email
        subject = "Verify Your GreenTrack Email"
        message = f"""
        Hello {user.username},
        
        Please verify your email address for your GreenTrack account.
        
        Click the link below to verify your email:
        {verify_url}
        
        Best regards,
        The GreenTrack Team
        """
        
        try:
            send_mail(
                subject,
                message,
                'noreply@greentrack.com',
                [user.email],
                fail_silently=False,
            )
            return Response({
                'message': 'Verification email sent successfully',
                'email': user.email
            })
        except Exception as e:
            return Response({
                'error': 'Failed to send verification email',
                'details': str(e)
            }, status=500)

class EmailVerificationConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        
        if not all([uid, token]):
            return Response({'error': 'All fields are required'}, status=400)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid verification link'}, status=400)
        
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired verification link'}, status=400)
        
        # Mark email as verified (you might want to add an email_verified field to your User model)
        # For now, we'll just return success
        return Response({'message': 'Email verified successfully'})

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
        
        return Response({'message': 'Password changed successfully'})

class TestUserView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        users = User.objects.all()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'date_joined': user.date_joined
            })
        return Response({'users': user_list})

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
