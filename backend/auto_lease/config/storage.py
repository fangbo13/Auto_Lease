from django.conf import settings
from django.core.files.storage import FileSystemStorage


def get_storage_backend():
    """获取当前配置的存储后端。"""
    storage_backend = getattr(settings, 'STORAGE_BACKEND', 'local')
    if storage_backend == 's3':
        try:
            from storages.backends.s3boto3 import S3Boto3Storage
            return S3Boto3Storage()
        except ImportError:
            pass
    return FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
