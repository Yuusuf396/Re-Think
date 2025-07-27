"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def test_view(request):
    """Simple test view to debug 400 errors"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Backend is working!',
        'allowed_hosts': request.get_host(),
        'debug': request.META.get('DEBUG', 'False')
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('tracker.urls')),
    path('test/', test_view, name='test'),
    path('', test_view, name='root'),
]
