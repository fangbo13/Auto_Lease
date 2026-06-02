import uuid
from django.db import models


class AuditTrail(models.Model):
    ACTION_CHOICES = [
        ('upload', '上传'),
        ('parse', '解析'),
        ('calculate', '计算'),
        ('export', '导出'),
        ('manual_create', '手动创建'),
        ('update', '更新'),
        ('delete', '删除'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='操作用户'
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='操作类型')
    entity_type = models.CharField(max_length=50, verbose_name='实体类型')
    entity_id = models.UUIDField(verbose_name='实体ID')
    details = models.JSONField(default=dict, blank=True, verbose_name='详情')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    class Meta:
        db_table = 'audit_trails'
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_action_display()} {self.entity_type} {self.entity_id}"
