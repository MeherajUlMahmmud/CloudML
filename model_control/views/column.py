from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from common.custom_view import CustomModelViewSet
from model_control.custom_filters import ColumnModelFilter
from model_control.models import ColumnModel, DatasetModel
from model_control.serializers.column import ColumnModelSerializer


class ColumnModelViewSet(CustomModelViewSet):
    http_method_names = ['get', 'head', 'options', 'patch', 'delete']
    queryset = ColumnModel.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_class = ColumnModelFilter

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ColumnModelSerializer.Write
        return ColumnModelSerializer.List

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ColumnModelSerializer.Details(instance)
        return Response(serializer.data)


class UpdateColumnModelAPIView(UpdateAPIView):
    http_method_names = ['patch']
    queryset = DatasetModel.objects.all()
    serializer_class = ColumnModelSerializer.BulkUpdate
    lookup_field = 'dataset_id'

    def patch(self, request, *args, **kwargs):
        dataset_id = kwargs['dataset_id']
        dataset_model = DatasetModel.objects.get(id=dataset_id)

        columns = request.data.get('columns')

        try:
            for column_data in columns:
                column_model = ColumnModel.objects.get(id=column_data['id'], dataset_model=dataset_model)
                serializer = ColumnModelSerializer.Write(column_model, data=column_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Update DataFrame
            import pandas as pd
            dataframe = pd.read_csv(dataset_model.dataset.path)
            dataframe.columns = [column['name'] for column in columns]
            dataframe.to_csv(dataset_model.dataset.path, index=False)

            return Response({
                'message': 'Columns updated successfully',
            }, status=status.HTTP_200_OK)

        except ColumnModel.DoesNotExist:
            return Response({'message': 'Column not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
