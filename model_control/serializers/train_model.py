from rest_framework.serializers import ModelSerializer

from common.choices import TrainModelTypeChoices
from model_control.models import TrainModel
from model_control.serializers.dataset import DatasetModelSerializer
from model_control.serializers.project import ProjectModelSerializer


class TrainModelSerializerMeta(ModelSerializer):
    class Meta:
        model = TrainModel
        fields = [
            'name',
            'description',
            'dataset_model',
            'project_model',
            'model_type',
            'test_size',
        ]


class TrainModelSerializer:
    class List(TrainModelSerializerMeta):
        class Meta(TrainModelSerializerMeta.Meta):
            fields = TrainModelSerializerMeta.Meta.fields + [
                'id',
                'model',
                'metrics',
                'plots',
                'is_training',
                'is_complete',
                'created_at',
                'updated_at',
            ]

    class Details(TrainModelSerializerMeta):
        dataset_model = DatasetModelSerializer.Lite()
        project_model = ProjectModelSerializer.Lite()

        class Meta(TrainModelSerializerMeta.Meta):
            fields = TrainModelSerializerMeta.Meta.fields + [
                'id',
                'model',
                'hyperparameters',
                'metrics',
                'plots',
                'is_training',
                'is_complete',
                'is_active',
                'is_deleted',
                'created_at',
                'updated_at',
            ]

    class Lite(TrainModelSerializerMeta):
        class Meta(TrainModelSerializerMeta.Meta):
            fields = TrainModelSerializerMeta.Meta.fields + [
                'id',
                'is_training',
                'is_complete',
            ]

    class Write(TrainModelSerializerMeta):
        class Meta(TrainModelSerializerMeta.Meta):
            fields = TrainModelSerializerMeta.Meta.fields + [
            ]

        def validate(self, attrs):
            model_type = attrs.get('model_type')
            if model_type != TrainModelTypeChoices.LINEAR_REGRESSION:
                raise Exception('We only support Linear Regression for now')
            return attrs

    class Task(TrainModelSerializerMeta):
        class Meta(TrainModelSerializerMeta.Meta):
            fields = TrainModelSerializerMeta.Meta.fields + [
            ]
