from rest_framework import generics
from rest_framework.response import Response
from .models import CalculationResult, AmortizationSchedule
from .serializers import CalculationResultSerializer, AmortizationScheduleSerializer, CalculationTriggerSerializer
from core.pagination import StandardResultsSetPagination


class CalculationTriggerView(generics.GenericAPIView):
    serializer_class = CalculationTriggerSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': '请使用 /api/lease-inputs/{id}/calculate/ 触发计算'})


class CalculationResultDetailView(generics.RetrieveAPIView):
    queryset = CalculationResult.objects.all()
    serializer_class = CalculationResultSerializer
    lookup_field = 'pk'


class AmortizationScheduleListView(generics.ListAPIView):
    serializer_class = AmortizationScheduleSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        result_id = self.kwargs.get('pk')
        return AmortizationSchedule.objects.filter(calculation_result_id=result_id)
