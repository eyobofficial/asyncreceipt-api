"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework import permissions, authentication

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Receipts API",
      default_version='v1.0.0',
      description=(
          'RESTful API for generating multiple receipts asynchronously for ' \
          'authenticated and authorized users. Receipts are generated in '\
          'JSON and PDF formats.'
      ),
      contact=openapi.Contact(email="hello@eyob.tech"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny]
)


# Schema URLS
urlpatterns = [
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Root URLs
urlpatterns += [
    path('receipts/', include('receipts.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('auth/register/', include('rest_auth.registration.urls')),
]

# Media Assets
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Update Admin Site Title
admin.site.site_header = admin.site.site_title = settings.PROJECT_NAME
admin.site.enable_nav_sidebar = False
