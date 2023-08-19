from rest_framework.serializers import ModelSerializer

from model_control.models import ColumnModel


class ColumnModelSerializerMeta(ModelSerializer):
    class Meta:
        model = ColumnModel
        fields = [
            'name',
            'description',
            'dataset_model',
            'encoding_type',
            'scaling_type',
            'is_numeric',
            'is_feature',
            'is_target',
        ]


class ColumnModelSerializer:
    class List(ColumnModelSerializerMeta):
        class Meta(ColumnModelSerializerMeta.Meta):
            fields = ColumnModelSerializerMeta.Meta.fields + [
                'id',
            ]

    class Details(ColumnModelSerializerMeta):
        class Meta(ColumnModelSerializerMeta.Meta):
            fields = ColumnModelSerializerMeta.Meta.fields + [
                'id',
                'is_active',
                'is_deleted',
                'created_at',
                'updated_at',
            ]

    class Lite(ColumnModelSerializerMeta):
        class Meta(ColumnModelSerializerMeta.Meta):
            fields = ColumnModelSerializerMeta.Meta.fields + [
                'id',
            ]

    class Write(ColumnModelSerializerMeta):
        class Meta(ColumnModelSerializerMeta.Meta):
            fields = ColumnModelSerializerMeta.Meta.fields + [
            ]

    class BulkUpdate(ColumnModelSerializerMeta):
        columns = ColumnModelSerializerMeta(many=True)

        class Meta(ColumnModelSerializerMeta.Meta):
            fields = [
                'columns',
            ]
