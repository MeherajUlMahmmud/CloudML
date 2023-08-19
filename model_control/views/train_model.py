from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from common.custom_view import CustomModelViewSet
from model_control.custom_filters import TrainModelFilter
from model_control.models import TrainModel
from model_control.serializers.train_model import TrainModelSerializer
from model_control.tasks import preprocess_and_train_model


class TrainModelViewSet(CustomModelViewSet):
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']
    queryset = TrainModel.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_class = TrainModelFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return TrainModelSerializer.Write
        return TrainModelSerializer.List

    def get_queryset(self):
        queryset = super().get_queryset()
        # Retrieve the search parameter from the query
        dataset_model = self.request.query_params.get('dataset_model', None)

        # If a search query is provided, filter by product_name, barcode, or manufacturer_name
        if dataset_model:
            # Initially try searching by product_name, barcode, and manufacturer_name
            filtered_queryset = queryset.filter(dataset_model=dataset_model)

            queryset = filtered_queryset

        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = TrainModelSerializer.Write(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.is_training = True
        instance.save()

        train_model_instance_id = instance.id
        preprocess_and_train_model.delay(train_model_instance_id)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TrainModelSerializer.Details(instance)
        return Response(serializer.data)
