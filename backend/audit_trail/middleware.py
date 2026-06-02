from .models import AuditTrail


class AuditTrailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 记录 IP 地址到 request，供后续视图使用
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request.ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            request.ip_address = request.META.get('REMOTE_ADDR')

        response = self.get_response(request)
        return response
