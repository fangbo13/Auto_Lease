from django.contrib import admin
from .models import AuditTrail


@admin.register(AuditTrail)
class AuditTrailAdmin(admin.ModelAdmin):
    list_display = ['action', 'entity_type', 'entity_id', 'user', 'ip_address', 'timestamp']
    list_filter = ['action', 'entity_type', 'timestamp']
    search_fields = ['entity_id', 'details']
    readonly_fields = [f.name for f in AuditTrail._meta.fields]
    date_hierarchy = 'timestamp'
