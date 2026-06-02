from django.urls import path
from .views import ExportWorkingPaperView

urlpatterns = [
    path('working-paper/', ExportWorkingPaperView.as_view(), name='export-working-paper'),
]
