from rest_framework.serializers import ModelSerializer

from model_control.models import ProjectModel
from user_control.serializers.user import UserModelSerializer


class ProjectModelSerializerMeta(ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = [
            'name',
            'description',
        ]


class ProjectModelSerializer:
    class List(ProjectModelSerializerMeta):
        class Meta(ProjectModelSerializerMeta.Meta):
            fields = ProjectModelSerializerMeta.Meta.fields + [
                'id',
                'user',
                'created_at',
                'updated_at',
            ]

    class Details(ProjectModelSerializerMeta):
        user = UserModelSerializer.List()

        class Meta(ProjectModelSerializerMeta.Meta):
            fields = ProjectModelSerializerMeta.Meta.fields + [
                'id',
                'user',
                'is_active',
                'is_deleted',
                'created_at',
                'updated_at',
            ]

    class Lite(ProjectModelSerializerMeta):
        class Meta(ProjectModelSerializerMeta.Meta):
            fields = ProjectModelSerializerMeta.Meta.fields + [
                'id',
            ]

    class Write(ProjectModelSerializerMeta):
        class Meta(ProjectModelSerializerMeta.Meta):
            fields = ProjectModelSerializerMeta.Meta.fields + [
                'user',
            ]

        # def create(self, validated_data):
        #     print(validated_data)
        #     return ProjectModel.objects.create(**validated_data)
