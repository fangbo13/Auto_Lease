from rest_framework import serializers
from .models import CalculationResult, AmortizationSchedule


class CalculationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationResult
        fields = [
            'id', 'lease_input', 'right_of_use_asset', 'lease_liability',
            'total_payments', 'total_interest', 'total_depreciation',
            'first_month_interest', 'first_month_depreciation',
            'effective_monthly_rate', 'calculated_at', 'created_at'
        ]
        read_only_fields = fields


class AmortizationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmortizationSchedule
        fields = [
            'id', 'calculation_result', 'period_number', 'period_start_date',
            'period_end_date', 'opening_liability', 'payment_amount',
            'interest_expense', 'principal_reduction', 'closing_liability',
            'rou_asset_opening', 'depreciation_expense', 'rou_asset_closing'
        ]
        read_only_fields = fields


class CalculationTriggerSerializer(serializers.Serializer):
    lease_input_id = serializers.UUIDField(required=True)
