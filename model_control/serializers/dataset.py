from rest_framework.serializers import ModelSerializer

from model_control.models import DatasetModel
from model_control.serializers.project import ProjectModelSerializer


class DatasetModelSerializerMeta(ModelSerializer):
    class Meta:
        model = DatasetModel
        fields = [
            'name',
            'description',
        ]


class DatasetModelSerializer:
    class List(DatasetModelSerializerMeta):

        class Meta(DatasetModelSerializerMeta.Meta):
            fields = DatasetModelSerializerMeta.Meta.fields + [
                'id',
                'dataset',
                'dataset_size',
                'project_model',
                'created_at',
                'updated_at',
            ]

    class Details(DatasetModelSerializerMeta):
        project_model = ProjectModelSerializer.Lite()

        class Meta(DatasetModelSerializerMeta.Meta):
            fields = DatasetModelSerializerMeta.Meta.fields + [
                'id',
                'dataset',
                'dataset_size',
                'project_model',
                'is_active',
                'is_deleted',
                'created_at',
                'updated_at',
            ]

    class Lite(DatasetModelSerializerMeta):
        project_model = ProjectModelSerializer.Lite()

        class Meta(DatasetModelSerializerMeta.Meta):
            fields = DatasetModelSerializerMeta.Meta.fields + [
                'id',
                'project_model',
            ]

    class Write(DatasetModelSerializerMeta):
        class Meta(DatasetModelSerializerMeta.Meta):
            fields = DatasetModelSerializerMeta.Meta.fields + [
                'dataset',
                'dataset_size',
                'project_model',
            ]

        def validate(self, attrs):
            dataset = attrs.get('dataset')
            if dataset.name.split('.')[-1] not in ['csv', 'xlsx']:
                raise ValueError('Only csv and xlsx files are allowed')
            if dataset.size > 1024 * 1024 * 10:  # 10MB
                raise ValueError('Maximum file size is 10MB')
            return attrs

    class Update(DatasetModelSerializerMeta):
        class Meta(DatasetModelSerializerMeta.Meta):
            fields = DatasetModelSerializerMeta.Meta.fields + [
            ]
