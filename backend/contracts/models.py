from django.db import models
from core.models import AbstractTimestampModel


class Contract(AbstractTimestampModel):
    PARSE_STATUS_CHOICES = [
        ('uploaded', '已上传'),
        ('parsing', '解析中'),
        ('success', '解析成功'),
        ('failed', '解析失败'),
    ]

    original_file = models.FileField(upload_to='contracts/%Y/%m/', verbose_name='原始文件')
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_size = models.PositiveIntegerField(verbose_name='文件大小(字节)')
    mime_type = models.CharField(max_length=100, verbose_name='MIME类型')
    uploaded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='上传用户'
    )
    parsed_status = models.CharField(
        max_length=20,
        choices=PARSE_STATUS_CHOICES,
        default='uploaded',
        verbose_name='解析状态'
    )
    parser_used = models.CharField(max_length=50, blank=True, verbose_name='所用解析器')
    parsed_text = models.TextField(blank=True, verbose_name='解析出的原始文本')
    parsed_data = models.JSONField(default=dict, blank=True, verbose_name='解析结果(JSON)')

    class Meta:
        db_table = 'contracts'
        verbose_name = '合同'
        verbose_name_plural = '合同'

    def __str__(self):
        return self.file_name
