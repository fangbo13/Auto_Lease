from django.contrib import admin
from .models import CalculationResult, AmortizationSchedule


class AmortizationScheduleInline(admin.TabularInline):
    model = AmortizationSchedule
    extra = 0
    readonly_fields = [f.name for f in AmortizationSchedule._meta.fields if f.name not in ['id']]
    can_delete = False


@admin.register(CalculationResult)
class CalculationResultAdmin(admin.ModelAdmin):
    list_display = [
        'lease_input', 'right_of_use_asset', 'lease_liability',
        'total_interest', 'total_depreciation', 'calculated_at'
    ]
    readonly_fields = ['id', 'calculated_at', 'created_at', 'updated_at']
    inlines = [AmortizationScheduleInline]


@admin.register(AmortizationSchedule)
class AmortizationScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'calculation_result', 'period_number', 'period_start_date',
        'opening_liability', 'interest_expense', 'principal_reduction',
        'closing_liability', 'depreciation_expense', 'rou_asset_closing'
    ]
    list_filter = ['calculation_result']
    readonly_fields = ['id', 'created_at', 'updated_at']
