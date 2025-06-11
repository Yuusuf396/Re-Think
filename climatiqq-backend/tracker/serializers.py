from rest_framework import serializers

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ImpactEntry

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class ImpactEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactEntry
        fields = ['id', 'metric_type', 'value', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class DashboardSerializer(serializers.Serializer):
     
    metric_type = serializers.CharField()
    total_value = serializers.FloatField()
    entry_count = serializers.IntegerField()
    last_entry_date = serializers.DateTimeField()



# # serializers.py
# from rest_framework import serializers
# from .models import ImpactLog, UserProfile, Challenge, UserChallenge, ImpactCategory, Tip

# class ImpactLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImpactLog
#         fields = '__all__'
#         read_only_fields = ['user', 'timestamp', 'unit']
    
#     def create(self, validated_data):
#         validated_data['user'] = self.context['request'].user
#         return super().create(validated_data)

# class UserProfileSerializer(serializers.ModelSerializer):
#     monthly_summary = serializers.SerializerMethodField()
    
#     class Meta:
#         model = UserProfile
#         exclude = ['user']
    
#     def get_monthly_summary(self, obj):
#         return obj.get_monthly_impact_summary()

# class ChallengeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Challenge
#         fields = '__all__'

# class UserChallengeSerializer(serializers.ModelSerializer):
#     challenge_details = ChallengeSerializer(source='challenge', read_only=True)
#     progress = serializers.SerializerMethodField()
    
#     class Meta:
#         model = UserChallenge
#         fields = '__all__'
#         read_only_fields = ['user', 'end_date', 'is_completed']
    
#     def get_progress(self, obj):
#         return obj.progress_percentage()

# class ImpactCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImpactCategory
#         fields = '__all__'

# class TipSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tip
#         fields = '__all__'

# # views.py
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.utils import timezone
# from datetime import timedelta

# class ImpactLogViewSet(viewsets.ModelViewSet):
#     serializer_class = ImpactLogSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return ImpactLog.objects.filter(user=self.request.user).order_by('-timestamp')
    
#     @action(detail=False, methods=['get'])
#     def weekly_summary(self, request):
#         """Get last 7 days impact summary"""
#         week_ago = timezone.now() - timedelta(days=7)
#         logs = self.get_queryset().filter(timestamp__gte=week_ago)
        
#         summary = {}
#         for metric in ['carbon', 'water', 'energy']:
#             metric_logs = logs.filter(metric_type=metric)
#             positive = sum(log.value for log in metric_logs if log.is_positive_impact)
#             negative = sum(log.value for log in metric_logs if not log.is_positive_impact)
#             summary[metric] = {
#                 'positive': positive,
#                 'negative': negative,
#                 'net': positive - negative,
#                 'count': metric_logs.count()
#             }
        
#         return Response(summary)
    
#     @action(detail=False, methods=['post'])
#     def quick_log(self, request):
#         """Quick logging endpoint for common actions"""
#         quick_actions = {
#             'bike_to_work': {'metric_type': 'carbon', 'value': 5, 'description': 'Biked to work'},
#             'recycled': {'metric_type': 'waste', 'value': 1, 'description': 'Recycled items'},
#             'shorter_shower': {'metric_type': 'water', 'value': 20, 'description': 'Took shorter shower'},
#         }
        
#         action_type = request.data.get('action')
#         if action_type not in quick_actions:
#             return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
#         log_data = quick_actions[action_type].copy()
#         log_data['user'] = request.user
#         log_data['is_positive_impact'] = True
        
#         log = ImpactLog.objects.create(**log_data)
#         return Response(ImpactLogSerializer(log).data, status=status.HTTP_201_CREATED)

# class UserProfileViewSet(viewsets.ModelViewSet):
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return UserProfile.objects.filter(user=self.request.user)
    
#     @action(detail=False, methods=['get'])
#     def dashboard(self, request):
#         """Main dashboard data"""
#         try:
#             profile = UserProfile.objects.get(user=request.user)
#         except UserProfile.DoesNotExist:
#             return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         # Recent logs
#         recent_logs = ImpactLog.objects.filter(user=request.user)[:5]
        
#         # Active challenges
#         active_challenges = UserChallenge.objects.filter(
#             user=request.user,
#             is_completed=False,
#             end_date__gte=timezone.now()
#         )
        
#         # Monthly progress
#         monthly_summary = profile.get_monthly_impact_summary()
        
#         return Response({
#             'profile': UserProfileSerializer(profile).data,
#             'recent_logs': ImpactLogSerializer(recent_logs, many=True).data,
#             'active_challenges': UserChallengeSerializer(active_challenges, many=True).data,
#             'monthly_summary': monthly_summary,
#         })

# class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = ChallengeSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Challenge.objects.filter(is_active=True)
    
#     @action(detail=True, methods=['post'])
#     def join(self, request, pk=None):
#         """Join a challenge"""
#         challenge = self.get_object()
#         user_challenge, created = UserChallenge.objects.get_or_create(
#             user=request.user,
#             challenge=challenge
#         )
        
#         if not created:
#             return Response({'error': 'Already joined this challenge'}, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response(UserChallengeSerializer(user_challenge).data, status=status.HTTP_201_CREATED)

# class TipViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = TipSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Tip.objects.filter(is_active=True)
    
#     @action(detail=False, methods=['get'])
#     def personalized(self, request):
#         """Get personalized tips based on user's primary focus"""
#         try:
#             profile = UserProfile.objects.get(user=request.user)
#             tips = self.queryset.filter(metric_type=profile.primary_focus)[:5]
#             return Response(TipSerializer(tips, many=True).data)
#         except UserProfile.DoesNotExist:
#             return Response(TipSerializer(self.queryset[:5], many=True).data)