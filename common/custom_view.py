from django.utils import timezone
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class CustomModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            created_at=timezone.now()
        )

    def perform_update(self, serializer):
        serializer.save(
            updated_at=timezone.now()
        )


class CustomCreateAPIView(CreateAPIView):
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_at=timezone.now())


class CustomUpdateAPIView(UpdateAPIView):
    http_method_names = ['put', 'patch']
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())
