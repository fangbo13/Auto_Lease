from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'mime_type', 'parsed_status', 'parser_used', 'uploaded_by', 'created_at']
    list_filter = ['parsed_status', 'mime_type', 'created_at']
    search_fields = ['file_name', 'parsed_text']
    readonly_fields = ['id', 'created_at', 'updated_at']
