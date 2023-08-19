import pandas as pd
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from common.custom_view import CustomModelViewSet
from model_control.models import DatasetModel, ColumnModel
from model_control.serializers.column import ColumnModelSerializer
from model_control.serializers.dataset import DatasetModelSerializer
from model_control.utils import get_numeric_columns, get_categorical_columns


class DatasetModelViewSet(CustomModelViewSet):
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']
    queryset = DatasetModel.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DatasetModelSerializer.Write
        elif self.request.method == 'PATCH':
            return DatasetModelSerializer.Update
        return DatasetModelSerializer.List

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        instance = serializer.save()
        serializer = DatasetModelSerializer.Details(instance)

        # calculate size of dataset
        dataset = instance.dataset
        dataset_size = dataset.size
        dataset_size = dataset_size / 1024 / 1024  # convert to MB
        dataset_size = round(dataset_size, 2)
        instance.dataset_size = dataset_size
        instance.save()

        column_dict = process_dataset(dataset)
        print(column_dict)

        for column_name, column_type in column_dict.items():
            column = ColumnModel.objects.create(
                dataset_model=instance,
                name=column_name,
                is_numeric=column_type == 'numeric',
            )
            column.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        dataset = self.get_object()
        columns = dataset.column_models.all()
        dataset_obj = DatasetModel.objects.get(id=dataset.id)
        dataset_serializer = DatasetModelSerializer.Details(dataset)
        column_serializer = ColumnModelSerializer.Details(columns, many=True)
        return Response({
            'dataset': dataset_serializer.data,
            'columns': column_serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_column_model(instance)
        instance.dataset.delete()
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)


def process_dataset(dataset):
    df = pd.read_csv(dataset)
    columns = df.columns

    numeric_columns = get_numeric_columns(df)
    categorical_columns = get_categorical_columns(df)

    column_dict = {}
    for column in columns:
        if column in numeric_columns:
            column_dict[column] = 'numeric'
        elif column in categorical_columns:
            column_dict[column] = 'categorical'
        else:
            column_dict[column] = 'unknown'

    return column_dict


def delete_column_model(instance):
    columns = ColumnModel.objects.filter(dataset_model=instance)
    for column in columns:
        column.delete()
