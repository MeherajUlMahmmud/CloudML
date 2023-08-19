from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from common.custom_view import CustomModelViewSet
from user_control.custom_filters import UserModelFilter
from user_control.models import UserModel
from user_control.serializers.user import UserModelSerializer


class UserModelViewSet(CustomModelViewSet):
    http_method_names = ['get', 'options', 'head', 'post', 'patch', 'delete']
    queryset = UserModel.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filterset_class = UserModelFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return UserModelSerializer.Write
        return UserModelSerializer.List
