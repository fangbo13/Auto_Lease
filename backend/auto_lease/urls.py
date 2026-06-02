"""
URL configuration for auto_lease project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/contracts/', include('contracts.urls')),
    path('api/lease-inputs/', include('lease_input.urls')),
    path('api/calculate/', include('calculations.urls')),
    path('api/export/', include('excel_export.urls')),
    path('api/audit/', include('audit_trail.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
