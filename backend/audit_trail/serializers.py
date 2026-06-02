from rest_framework import serializers
from .models import AuditTrail


class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = [
            'id', 'user', 'action', 'entity_type', 'entity_id',
            'details', 'ip_address', 'timestamp'
        ]
        read_only_fields = fields
