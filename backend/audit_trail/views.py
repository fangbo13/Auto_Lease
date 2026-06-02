from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import AuditTrail
from .serializers import AuditTrailSerializer


class AuditTrailListView(generics.ListAPIView):
    queryset = AuditTrail.objects.all()
    serializer_class = AuditTrailSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        action = self.request.query_params.get('action')
        entity_type = self.request.query_params.get('entity_type')
        if action:
            queryset = queryset.filter(action=action)
        if entity_type:
            queryset = queryset.filter(entity_type=entity_type)
        return queryset
