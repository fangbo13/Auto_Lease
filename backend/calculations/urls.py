from django.urls import path
from .views import (
    CalculationTriggerView,
    CalculationResultDetailView,
    AmortizationScheduleListView,
)

urlpatterns = [
    path('trigger/', CalculationTriggerView.as_view(), name='calculation-trigger'),
    path('results/<uuid:pk>/', CalculationResultDetailView.as_view(), name='calculation-result-detail'),
    path('results/<uuid:pk>/schedule/', AmortizationScheduleListView.as_view(), name='amortization-schedule'),
]
