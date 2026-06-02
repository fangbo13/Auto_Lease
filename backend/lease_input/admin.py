from django.contrib import admin
from .models import LeaseInput


@admin.register(LeaseInput)
class LeaseInputAdmin(admin.ModelAdmin):
    list_display = [
        'lease_name', 'lease_commencement_date', 'lease_term_months',
        'payment_frequency', 'payment_amount', 'discount_rate', 'standard', 'created_at'
    ]
    list_filter = ['standard', 'payment_frequency', 'payment_timing', 'created_at']
    search_fields = ['lease_name', 'notes']
    readonly_fields = ['id', 'created_at', 'updated_at']
