from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from common.custom_permission import AdminOrStaffUserPermission
from common.custom_view import (
    CustomCreateAPIView, CustomUpdateAPIView, CustomRetrieveAPIView, CustomListAPIView,
)
from common.utils import save_picture_to_folder
from user_control.custom_filters import UserModelFilter
from user_control.models import UserModel
from user_control.serializers.user import UserModelSerializer


class GetUserListAPIView(CustomListAPIView):
    queryset = UserModel.objects.filter(is_active=True, is_deleted=False)
    permission_classes = [AdminOrStaffUserPermission]
    serializer_class = UserModelSerializer.List
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = UserModelFilter
    search_fields = ['email', 'first_name', 'last_name']


class GetUserDetailsAPIView(CustomRetrieveAPIView):
    queryset = UserModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = UserModelSerializer.List

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user
        if not request.user.check_object_permissions(request, instance) and not requested_user.id == instance.id:
            return Response({
                'detail': 'You don\'t have permission to perform this action.'
            }, status=HTTP_403_FORBIDDEN)

        serializer = UserModelSerializer.List(instance)
        return Response({
            'data': serializer.data,
        }, status=HTTP_200_OK)


class GetUserProfileAPIView(CustomRetrieveAPIView):

    def get(self, request, *args, **kwargs):
        instance = request.user
        if not request.user.check_object_permissions(request, instance) and not request.user.id == instance.id:
            return Response({
                'message': 'You don\'t have permission to perform this action.'
            }, status=HTTP_403_FORBIDDEN)

        serializer = UserModelSerializer.List(instance)
        return Response(serializer.data, status=HTTP_200_OK)


class CreateUserAPIView(CustomCreateAPIView):
    permission_classes = (AdminOrStaffUserPermission,)
    queryset = UserModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = UserModelSerializer.Write

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        password = validated_data['password']

        user = UserModel.objects.create(
            created_by=request.user,
            **validated_data
        )
        user.set_password(password)
        user.save()

        return Response({
            'message': 'User created successfully.',
        }, status=HTTP_201_CREATED)


class UpdateUserDetailsAPIView(CustomUpdateAPIView):
    queryset = UserModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = UserModelSerializer.Write

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user
        if not request.user.check_object_permissions(request, instance) and not requested_user.id == instance.id:
            return Response({
                'message': 'You don\'t have permission to perform this action.'
            }, status=HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            updated_by=request.user,
        )
        return Response(serializer.data, status=HTTP_200_OK)


class UpdateProfilePictureAPIView(CustomUpdateAPIView):
    queryset = UserModel.objects.filter(is_active=True, is_deleted=False)
    serializer_class = UserModelSerializer.UpdateProfilePicture

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        requested_user = request.user
        if not request.user.check_object_permissions(request, instance) and not requested_user.id == instance.id:
            return Response({
                'message': 'You do not have permission to perform this action.'
            }, status=HTTP_403_FORBIDDEN)

        data = request.data
        serializer = self.serializer_class(instance, data=data)
        serializer.is_valid(raise_exception=True)
        profile_picture = request.FILES.get('profile_picture')
        picture_path = save_picture_to_folder(
            profile_picture, 'profile_pictures')
        serializer.validated_data['profile_picture'] = picture_path
        serializer.save(
            updated_by=request.user,
        )
        return Response({
            'data': picture_path,
        }, status=HTTP_200_OK)
