from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LeaseInput
from .serializers import LeaseInputSerializer, LeaseInputCreateSerializer, LeaseInputListSerializer
from calculations.services.ifrs16_engine import IFRS16Engine
from calculations.models import CalculationResult, AmortizationSchedule
from audit_trail.models import AuditTrail


class LeaseInputViewSet(viewsets.ModelViewSet):
    queryset = LeaseInput.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return LeaseInputListSerializer
        if self.action == 'create':
            return LeaseInputCreateSerializer
        return LeaseInputSerializer

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)
        AuditTrail.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action='manual_create',
            entity_type='LeaseInput',
            entity_id=instance.id,
            details={'lease_name': instance.lease_name}
        )
        return instance

    @action(detail=True, methods=['post'], url_path='calculate')
    def calculate(self, request, pk=None):
        lease_input = self.get_object()

        try:
            engine = IFRS16Engine(lease_input)
            result = engine.calculate()

            CalculationResult.objects.filter(lease_input=lease_input).delete()

            calc_result = CalculationResult.objects.create(
                lease_input=lease_input,
                right_of_use_asset=result['right_of_use_asset'],
                lease_liability=result['lease_liability'],
                total_payments=result['total_payments'],
                total_interest=result['total_interest'],
                total_depreciation=result['total_depreciation'],
                first_month_interest=result['first_month_interest'],
                first_month_depreciation=result['first_month_depreciation'],
                effective_monthly_rate=result['effective_monthly_rate'],
            )

            schedule_rows = []
            for row in result['schedule']:
                schedule_rows.append(AmortizationSchedule(
                    calculation_result=calc_result,
                    period_number=row['period_number'],
                    period_start_date=row['period_start_date'],
                    period_end_date=row['period_end_date'],
                    opening_liability=row['opening_liability'],
                    payment_amount=row['payment_amount'],
                    interest_expense=row['interest_expense'],
                    principal_reduction=row['principal_reduction'],
                    closing_liability=row['closing_liability'],
                    rou_asset_opening=row['rou_asset_opening'],
                    depreciation_expense=row['depreciation_expense'],
                    rou_asset_closing=row['rou_asset_closing'],
                ))
            AmortizationSchedule.objects.bulk_create(schedule_rows)

            AuditTrail.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action='calculate',
                entity_type='LeaseInput',
                entity_id=lease_input.id,
                details={'result_id': str(calc_result.id), 'rou_asset': str(calc_result.right_of_use_asset)}
            )

            return Response({
                'id': str(calc_result.id),
                'right_of_use_asset': str(calc_result.right_of_use_asset),
                'lease_liability': str(calc_result.lease_liability),
                'total_payments': str(calc_result.total_payments),
                'total_interest': str(calc_result.total_interest),
                'total_depreciation': str(calc_result.total_depreciation),
                'first_month_interest': str(calc_result.first_month_interest),
                'first_month_depreciation': str(calc_result.first_month_depreciation),
                'effective_monthly_rate': str(calc_result.effective_monthly_rate),
                'schedule_count': len(schedule_rows),
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
