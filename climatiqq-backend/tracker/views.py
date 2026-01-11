from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta

from .serializers import UserRegistrationSerializer, ImpactEntrySerializer
from .models import ImpactEntry

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'username': user.username,
                'email': user.email
            },
            'message': 'User registered successfully'
        }, status=201)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Standard JWT login view - uses username and password"""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get the user from the validated token
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user

            # Add user info to response
            response.data['user'] = {
                'username': user.username,
                'email': user.email
            }

        return response


# class ImpactEntryListCreateView(generics.ListCreateAPIView):
#     serializer_class = ImpactEntrySerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
       
#         queryset=ImpactEntry.objects.filter(user=self.request.user)
#         for entry in queryset:
#             print(entry.metric_type)  
        
#         return ImpactEntry.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
class ImpactEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = ImpactEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ImpactEntry.objects.filter(user=self.request.user)

        # Read query params
        metric_type = self.request.query_params.get('metric_type')
        if metric_type:
            queryset = queryset.filter(metric_type=metric_type)

        return queryset


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

        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_entries = entries.filter(created_at__gte=thirty_days_ago)

        total_entries = entries.count()
        recent_entries_count = recent_entries.count()

        metric_totals = entries.values('metric_type').annotate(
            total_value=Sum('value'),
            avg_value=Avg('value'),
            count=Count('id')
        )

        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_activity = entries.filter(
            created_at__gte=seven_days_ago).count()

        return Response({
            'total_entries': total_entries,
            'recent_entries': recent_entries_count,
            'recent_activity': recent_activity,
            'metric_breakdown': list(metric_totals),
        })
