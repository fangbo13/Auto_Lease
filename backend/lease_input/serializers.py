from rest_framework import serializers
from .models import LeaseInput


class LeaseInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseInput
        fields = [
            'id', 'contract', 'lease_name', 'lease_commencement_date',
            'lease_term_months', 'payment_frequency', 'payment_amount',
            'payment_timing', 'discount_rate', 'discount_rate_type',
            'tax_rate', 'initial_direct_costs', 'lease_incentives',
            'residual_value_guarantee', 'purchase_option', 'purchase_option_price',
            'standard', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('purchase_option') and not data.get('purchase_option_price'):
            raise serializers.ValidationError({'purchase_option_price': '启用购买选择权时必须填写价格。'})
        return data


class LeaseInputCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseInput
        fields = [
            'id', 'contract', 'lease_name', 'lease_commencement_date',
            'lease_term_months', 'payment_frequency', 'payment_amount',
            'payment_timing', 'discount_rate', 'discount_rate_type',
            'tax_rate', 'initial_direct_costs', 'lease_incentives',
            'residual_value_guarantee', 'purchase_option', 'purchase_option_price',
            'standard', 'notes'
        ]
        read_only_fields = ['id']

    def validate(self, data):
        if data.get('purchase_option') and not data.get('purchase_option_price'):
            raise serializers.ValidationError({'purchase_option_price': '启用购买选择权时必须填写价格。'})
        return data


class LeaseInputListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseInput
        fields = ['id', 'lease_name', 'lease_commencement_date', 'lease_term_months', 'payment_amount', 'created_at']
        read_only_fields = fields
