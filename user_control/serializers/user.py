from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user_control.models import UserModel


class UserModelSerializerMeta(ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'username',
            'is_admin',
            'is_staff',
            'is_superuser',
        ]


class UserModelSerializer:
    class List(UserModelSerializerMeta):
        class Meta(UserModelSerializerMeta.Meta):
            fields = UserModelSerializerMeta.Meta.fields + [
                'id',
                'created_at',
                'updated_at',
            ]

    class Write(UserModelSerializerMeta):
        password = serializers.CharField(write_only=True)

        class Meta(UserModelSerializerMeta.Meta):
            fields = UserModelSerializerMeta.Meta.fields + [
                'password',
            ]

        def create(self, validated_data):
            user = UserModel.objects.create(
                username=validated_data['username'],
            )
            user.set_password(validated_data['password'])
            user.save()

            return user

        def update(self, instance, validated_data):
            instance.username = validated_data['username']
            instance.is_admin = validated_data['is_admin']
            instance.is_staff = validated_data['is_staff']
            instance.is_superuser = validated_data['is_superuser']
            if 'password' in validated_data:
                instance.set_password(validated_data['password'])
            instance.save()

            return instance
