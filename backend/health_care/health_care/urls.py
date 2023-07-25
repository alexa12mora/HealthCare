"""
URL configuration for health_care project.

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
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include('admin_datta.urls')),
    # path('', include('django_dyn_dt.urls')), # <-- NEW: Dynamic_DT Routing   
    path('app/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', include('home.urls')),
    path("medical_reports", include("medical_reports.urls")),
]

# Lazy-load on routing is needed
# During the first build, API is not yet generated
try:
    urlpatterns.append(path("api/", include("api.urls")))
    urlpatterns.append(path("login/jwt/", view=obtain_auth_token))
except:
    pass