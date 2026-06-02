from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Contract
from .serializers import ContractUploadSerializer, ContractDetailSerializer, ContractParseSerializer
from ai_parser.registry import get_active_parser
from audit_trail.models import AuditTrail


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ContractUploadSerializer
        return ContractDetailSerializer

    def perform_create(self, serializer):
        instance = serializer.save(uploaded_by=self.request.user if self.request.user.is_authenticated else None)
        AuditTrail.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action='upload',
            entity_type='Contract',
            entity_id=instance.id,
            details={'file_name': instance.file_name, 'mime_type': instance.mime_type}
        )
        return instance

    @action(detail=True, methods=['post'], url_path='parse')
    def parse(self, request, pk=None):
        contract = self.get_object()
        serializer = ContractParseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parser_name = serializer.validated_data.get('parser', '')
        try:
            parser = get_active_parser(parser_name if parser_name else None)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        contract.parsed_status = 'parsing'
        contract.parser_used = parser.get_name()
        contract.save()

        try:
            result = parser.parse(contract.original_file.path, contract.mime_type)
            contract.parsed_data = result
            contract.parsed_status = 'success'
            contract.save()

            AuditTrail.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action='parse',
                entity_type='Contract',
                entity_id=contract.id,
                details={'parser': parser.get_name(), 'status': 'success'}
            )

            return Response({
                'status': 'success',
                'parser': parser.get_name(),
                'data': result
            })
        except Exception as e:
            contract.parsed_status = 'failed'
            contract.save()
            AuditTrail.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action='parse',
                entity_type='Contract',
                entity_id=contract.id,
                details={'parser': parser.get_name(), 'status': 'failed', 'error': str(e)}
            )
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
