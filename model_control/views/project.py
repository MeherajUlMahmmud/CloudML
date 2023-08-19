from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response

from common.custom_view import CustomModelViewSet
from model_control.models import ProjectModel
from model_control.serializers.dataset import DatasetModelSerializer
from model_control.serializers.project import ProjectModelSerializer


class ProjectModelViewSet(CustomModelViewSet):
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']
    queryset = ProjectModel.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return ProjectModelSerializer.Write
        return ProjectModelSerializer.List

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        datasets = project.dataset_models.all()
        project_serializer = ProjectModelSerializer.Details(project)
        dataset_serializer = DatasetModelSerializer.Details(datasets, many=True)
        return Response({
            'project': project_serializer.data,
            'datasets': dataset_serializer.data
        })
