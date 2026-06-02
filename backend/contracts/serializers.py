from rest_framework import serializers
from .models import Contract


class ContractUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'original_file', 'file_name', 'file_size', 'mime_type', 'parsed_status', 'created_at']
        read_only_fields = ['id', 'file_name', 'file_size', 'mime_type', 'parsed_status', 'created_at']

    def validate_original_file(self, value):
        valid_mime_types = [
            'application/pdf',
            'image/png',
            'image/jpeg',
            'image/jpg',
        ]
        if value.content_type not in valid_mime_types:
            raise serializers.ValidationError('仅支持 PDF、PNG、JPG 格式的文件。')
        if value.size > 20 * 1024 * 1024:
            raise serializers.ValidationError('文件大小不能超过 20MB。')
        return value

    def create(self, validated_data):
        file = validated_data['original_file']
        validated_data['file_name'] = file.name
        validated_data['file_size'] = file.size
        validated_data['mime_type'] = file.content_type
        return super().create(validated_data)


class ContractDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            'id', 'original_file', 'file_name', 'file_size', 'mime_type',
            'parsed_status', 'parser_used', 'parsed_data', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class ContractParseSerializer(serializers.Serializer):
    parser = serializers.CharField(required=False, allow_blank=True, help_text='指定解析器，为空则使用默认')
