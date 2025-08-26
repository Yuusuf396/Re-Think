from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta
import openai
import os

from .serializers import UserRegistrationSerializer, ImpactEntrySerializer
from .models import ImpactEntry
from .ai_model import carbon_ai_model
from .services.sendgrid_service import sendgrid_service

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Simple serializer for username-only login"""
    
    def validate(self, attrs):
        return super().validate(attrs)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            
            if response.status_code == 201:
                user_data = response.data
                try:
                    user = User.objects.get(username=user_data['username'])
                    
                    # Send welcome email using SendGrid
                    email_result = sendgrid_service.send_registration_email(user, request)
                    
                    # Generate JWT tokens for the new user
                    refresh = RefreshToken.for_user(user)
                    
                    response.data = {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': {
                            'username': user.username,
                            'email': user.email
                        },
                        'email_sent': email_result['success'],
                        'email_status': email_result.get('status_code'),
                        'message_id': email_result.get('message_id')
                    }
                    
                except User.DoesNotExist:
                    pass
            
            return response
        except Exception as e:
            print("Registration error:", str(e))
            raise

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
                    'carbon_footprint': entry.value if entry.metric_type == 'carbon' else 0,
                    'water_usage': entry.value if entry.metric_type == 'water' else 0,
                    'energy_usage': entry.value if entry.metric_type == 'energy' else 0,
                    'digital_usage': entry.value if entry.metric_type == 'digital' else 0,
                    'description': entry.description,
                    'created_at': entry.created_at.isoformat()
                }
                for entry in entries
            ]
        }
        
        try:
            # Use the global AI model instance
            result = carbon_ai_model.predict_suggestions(user_data)
            
            return Response({
                'suggestions': result.get('suggestions', []),
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
        
        # Send password change confirmation email
        email_result = sendgrid_service.send_password_change_confirmation(user)
        
        return Response({
            'message': 'Password changed successfully',
            'email_sent': email_result['success'],
            'email_status': email_result.get('status_code')
        })

class TestUserView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'message': 'API is working!',
            'status': 'success',
            'timestamp': timezone.now().isoformat()
        })

class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'message': 'Rethink API is running',
            'version': '1.0.0',
            'timestamp': timezone.now().isoformat()
        })

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

@login_required
def dashboard_view(request):
    """Web view for user dashboard"""
    user = request.user
    entries = ImpactEntry.objects.filter(user=user).order_by('-created_at')[:10]
    
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


class PasswordResetRequestView(APIView):
    """Request password reset via email"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email address is required'}, status=400)
        
        try:
            user = User.objects.get(email=email)
            result = sendgrid_service.send_password_reset_email(user, request)
            
            if result['success']:
                return Response({
                    'message': 'Password reset email sent successfully',
                    'email': email,
                    'status': 'success'
                })
            else:
                return Response({
                    'error': 'Failed to send email',
                    'details': result.get('error')
                }, status=500)
                
        except User.DoesNotExist:
            # Don't reveal if user exists or not for security
            return Response({
                'message': 'If an account exists with this email, a reset link has been sent.',
                'email': email,
                'status': 'success'
            })


class PasswordResetConfirmView(APIView):
    """Confirm password reset with token"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not all([uid, token, new_password]):
            return Response({
                'error': 'All fields are required: uid, token, new_password'
            }, status=400)
        
        # Validate the reset token
        validation_result = sendgrid_service.validate_reset_token(uid, token)
        
        if not validation_result['valid']:
            return Response({
                'error': validation_result['error']
            }, status=400)
        
        # Update user password
        user = validation_result['user']
        user.set_password(new_password)
        user.save()
        
        # Send confirmation email
        email_result = sendgrid_service.send_password_change_confirmation(user)
        
        return Response({
            'message': 'Password reset successfully',
            'email_sent': email_result['success'],
            'status': 'success'
        })
