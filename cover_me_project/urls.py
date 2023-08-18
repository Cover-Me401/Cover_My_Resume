"""
URL configuration for cover_me_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework_simplejwt import views as jwt_views
from .views import MyTokenObtainPairView
from django.views.generic.base import TemplateView
from . import views
from cover_me_app.views import uploadPDFView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cover_me_app/', include('cover_me_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  
    # ^These are for testing^- If using Django's built-in auth views
    path('admin/', admin.site.urls),
    path('api/v1/cover_me_app/', include('cover_me_app.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('account/', include('accounts.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('cover_me_app/', include('cover_me_app.urls')),
    # ADD upload-pdf to views.py
    path('upload-pdf', uploadPDFView), #SARAH I'm not sure
    path('accounts/', include('django.contrib.auth.urls')),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
