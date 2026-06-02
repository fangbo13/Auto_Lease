from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaseInputViewSet

router = DefaultRouter()
router.register(r'', LeaseInputViewSet, basename='leaseinput')

urlpatterns = [
    path('', include(router.urls)),
]
