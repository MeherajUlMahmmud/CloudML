from rest_framework.serializers import ModelSerializer

from user_control.models import CountryModel


class CountryModelSerializerMeta(ModelSerializer):
    class Meta:
        model = CountryModel
        ref_name = 'CountryModelSerializer'
        fields = [
            'id',
            'name',
        ]


class CountryModelSerializer:
    class List(CountryModelSerializerMeta):
        class Meta(CountryModelSerializerMeta.Meta):
            fields = CountryModelSerializerMeta.Meta.fields + [
                'description',
                'image',
                'created_at',
            ]

    class Lite(CountryModelSerializerMeta):
        class Meta(CountryModelSerializerMeta.Meta):
            fields = CountryModelSerializerMeta.Meta.fields

    class Write(CountryModelSerializerMeta):
        class Meta(CountryModelSerializerMeta.Meta):
            fields = CountryModelSerializerMeta.Meta.fields + [
                'name',
                'description',
                'image',
            ]
