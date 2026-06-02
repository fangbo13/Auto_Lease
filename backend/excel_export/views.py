from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lease_input.models import LeaseInput
from calculations.models import CalculationResult
from excel_export.services.chinese_audit_wp import ChineseAuditWorkingPaperGenerator
from audit_trail.models import AuditTrail


class ExportWorkingPaperView(APIView):
    def get(self, request):
        lease_input_id = request.query_params.get('lease_input_id')
        if not lease_input_id:
            return Response({'error': '缺少 lease_input_id 参数'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lease_input = LeaseInput.objects.get(id=lease_input_id)
        except LeaseInput.DoesNotExist:
            return Response({'error': 'LeaseInput 不存在'}, status=status.HTTP_404_NOT_FOUND)

        try:
            calculation_result = CalculationResult.objects.get(lease_input=lease_input)
        except CalculationResult.DoesNotExist:
            return Response({'error': '该租赁输入尚未计算，请先触发计算'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            generator = ChineseAuditWorkingPaperGenerator()
            excel_bytes = generator.generate(lease_input, calculation_result)
        except Exception as e:
            return Response({'error': f'Excel 生成失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        filename = f"租赁审计底稿_{lease_input.lease_name}_{lease_input.lease_commencement_date}.xlsx"

        AuditTrail.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='export',
            entity_type='LeaseInput',
            entity_id=lease_input.id,
            details={'filename': filename}
        )

        response = HttpResponse(excel_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
