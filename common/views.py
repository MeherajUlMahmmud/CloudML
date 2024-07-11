import logging
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from base import settings
from common.custom_view import CustomCreateAPIView
from common.utils import read_log_file
from .serializers import ContactUsSerializer

logger = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class LogAPIView(APIView):
    permission_classes = [IsAdminUser]  # Ensure only admins can access logs
    LOG_LINES_PER_PAGE = 200

    def get(self, request, *args, **kwargs):
        query_params = request.GET
        level = query_params.get('level', '')
        trace_id = query_params.get('trace_id', '')
        logs_per_page = int(query_params.get(
            'logs_per_page', self.LOG_LINES_PER_PAGE))
        page = int(query_params.get('page', 1))
        print(query_params)
        log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'debug.log')

        start_line = (page - 1) * logs_per_page
        end_line = page * logs_per_page
        print(start_line, end_line, trace_id, level)

        log_lines = read_log_file(log_file_path, end_line, trace_id, level)

        # Paginate log lines
        paginated_logs = log_lines[start_line:end_line]

        return JsonResponse({
            'logs': paginated_logs,
            'page': page,
            'total_pages': len(log_lines) // self.LOG_LINES_PER_PAGE + 1
        }, safe=False)


class ContactUsModelAPIView(CustomCreateAPIView):
    """
    API view to handle contact us form submissions.
    """
    permission_classes = [AllowAny, ]
    serializer_class = ContactUsSerializer

    def post(self, request):
        logger.info("Received contact us form submission")

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response({
                "message": "Thank you for contacting us! ❤️",
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error submitting contact us form: {e}")
            return Response({
                "message": "An error occurred while submitting the form.",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
