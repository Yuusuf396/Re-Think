from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, ProfileView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
] 