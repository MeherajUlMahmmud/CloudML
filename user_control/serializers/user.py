from rest_framework.serializers import ModelSerializer, CharField, ImageField

from user_control.serializers.country import CountryModelSerializer
from user_control.models import UserModel


class UserModelSerializerMeta(ModelSerializer):
    class Meta:
        model = UserModel
        ref_name = 'UserModelSerializer'
        fields = [
            'email',
            'first_name',
            'last_name',
            'auth_provider',
            'is_verified',
            'is_staff',
            'is_superuser',
        ]


class UserModelSerializer:
    class List(UserModelSerializerMeta):
        country = CountryModelSerializer.List(read_only=True)

        class Meta(UserModelSerializerMeta.Meta):
            fields = UserModelSerializerMeta.Meta.fields + [
                'id',
                'profile_picture',
                'country',
            ]

    class Lite(UserModelSerializerMeta):
        class Meta(UserModelSerializerMeta.Meta):
            fields = UserModelSerializerMeta.Meta.fields + [
                'id',
                'first_name',
                'last_name',
            ]

    class Write(UserModelSerializerMeta):
        first_name = CharField(write_only=True, required=True, )
        last_name = CharField(write_only=True, required=True, )
        password = CharField(write_only=True, required=True)

        class Meta(UserModelSerializerMeta.Meta):
            fields = UserModelSerializerMeta.Meta.fields + [
                'password',
            ]

    class UpdateProfilePicture(UserModelSerializerMeta):
        profile_picture = ImageField(required=True)

        class Meta(UserModelSerializerMeta.Meta):
            fields = [
                'profile_picture',
            ]
