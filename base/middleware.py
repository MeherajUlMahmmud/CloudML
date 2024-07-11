from common.models import RequestLog
from django.utils.deprecation import MiddlewareMixin
import uuid
from threading import local

_local = local()


class TraceIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        trace_id = uuid.uuid4().hex
        request.trace_id = trace_id
        _local.trace_id = trace_id

        response = self.get_response(request)
        return response


class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Log details at the start of the request if needed
        pass

    def process_response(self, request, response):
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        RequestLog.objects.create(
            user=user,
            ip_address=self.get_client_ip(request),
            endpoint=request.path,
            status_code=response.status_code,
            response=response.content.decode('utf-8')
        )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
