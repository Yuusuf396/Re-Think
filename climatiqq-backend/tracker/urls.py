from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .views import (
    RegisterView, CustomTokenObtainPairView,
    ImpactEntryListCreateView, ImpactEntryDetailView, ImpactStatsView
)

class LogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('entries/', ImpactEntryListCreateView.as_view(), name='entries'),
    path('entries/<int:pk>/', ImpactEntryDetailView.as_view(), name='entry_detail'),
    path('stats/', ImpactStatsView.as_view(), name='stats'),
] 