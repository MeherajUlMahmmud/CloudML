import logging
import os
from datetime import datetime, timedelta

import jwt
import pytz
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user_control.models import CountryModel
from user_control.models import UserModel
from user_control.serializers.auth import (
    RegisterSerializer, EmailVerificationSerializer, LoginSerializer,
    ResendVerificationEmailSerializer, LogoutSerializer, ResetPasswordRequestSerializer, SetNewPasswordSerializer,
)
from user_control.serializers.user import UserModelSerializer
from user_control.utils import Util

logger = logging.getLogger(__name__)


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @transaction.atomic
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password1 = data.get('password1')

            user = UserModel.objects.create_user(
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )

            try:
                # get country from ip address
                ip_address = Util.get_client_ip(request)
                country = Util.get_country_from_ip(ip_address)
                countries = CountryModel.objects.filter(code=country)
                if countries.exists():
                    user.country = countries.first()
                    user.save()
            except Exception as e:
                print(e)

            # name = first_name + " " + last_name
            # token = RefreshToken.for_user(user).access_token
            #
            # current_site = get_current_site(request).domain
            # relative_link = reverse('verify-email')
            # abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
            #
            # email_subject = 'Verify your email'
            # email_body = "Hi " + name + ",\nUse this link to verify your email:\n" + abs_url
            # email_data = {
            #     'email_subject': email_subject,
            #     'email_body': email_body,
            #     'to_email_list': [user.email],
            # }
            # Util.send_email(email_data)
            # send_mail(
            #     email_data['email_subject'],
            #     email_data['email_body'],
            #     'gktournament64@gmail.com',
            #     email_data['to_email_list'],
            #     fail_silently=False,
            # )

            return Response({
                'message': 'User registration successful',
            }, status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                'message': str(e),
            }, status=HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = get_object_or_404(UserModel, id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({
                'message': 'Email successfully verified',
            }, status=HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({
                'message': 'Activation Expired',
            }, status=HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({
                'message': 'Invalid token',
            }, status=HTTP_400_BAD_REQUEST)


class ResendVerificationEmailAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResendVerificationEmailSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        email = data.get('email')
        if email is None:
            return Response({
                'message': 'Please provide an email address',
            }, status=HTTP_400_BAD_REQUEST)
        user = get_object_or_404(UserModel, email=email)

        if user.is_verified:
            return Response({
                'message': 'Email already verified',
            }, status=HTTP_400_BAD_REQUEST)

        name = user.first_name + " " + user.last_name
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('verify-email')
        abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)

        email_subject = 'Verify your email'
        email_body = "Hi " + name + ",\nUse this link to verify your email:\n" + abs_url
        email_data = {
            'email_subject': email_subject,
            'email_body': email_body,
            'to_email': user.email,
        }
        Util.send_email(email_data)

        return Response({
            'message': 'Email sent successfully',
        }, status=HTTP_200_OK)


class LoginAPIView(GenericAPIView):
    """
    Handles user login functionality.

    - Allows any user to access this view.
    - Validates user credentials and returns authentication tokens.
    - Updates the user's last login time.
    - Optionally updates the user's country based on their IP address.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handles POST requests for user login.

        :param request: HTTP request object.
        :return: HTTP Response object with user data and tokens if successful,
                 otherwise an error message.
        """
        logger.info(f'User login attempt: {request.data}')

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        logger.info(f'User login serializer data: {serializer.validated_data}')

        user = serializer.validated_data['user']
        tokens = serializer.validated_data['tokens']

        if user:
            logger.info(f'User {user.email} found, updating last login time and user country.')
            user.update_last_login()
            user.update_user_country(request)

            logger.info(f'User {user.email} logged in successfully.')
            user_data = UserModelSerializer.List(user).data
            return Response({
                'message': 'Login successful',
                'user': user_data,
                'tokens': tokens,
            }, status=HTTP_200_OK)
        else:
            logger.error('Invalid credentials')
            return Response({
                'message': 'Invalid credentials',
            }, status=HTTP_400_BAD_REQUEST)


class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Logout successful',
        }, status=HTTP_204_NO_CONTENT)


class PasswordChangeAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['password1'])
        user.save()
        return Response({
            'message': 'Password changed successfully',
        }, status=HTTP_200_OK)


class RequestPasswordResetAPIView(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        email = data.get('email')

        user = get_object_or_404(UserModel, email=email)

        u_id_b64 = urlsafe_base64_encode(
            smart_bytes(user.id) + smart_bytes('||') + smart_bytes(user.email)
        )
        token = PasswordResetTokenGenerator().make_token(user)

        user.reset_password_token = token
        user.reset_password_token_expiry = datetime.now() + timedelta(minutes=5)
        user.save()

        return Response({
            'message': 'Password reset link sent successfully',
            'u_id_b64': u_id_b64,
            'token': token,
        }, status=HTTP_200_OK)

        # current_site = get_current_site(request).domain
        # relative_link = reverse(
        #     'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        #
        # redirect_url = request.data.get('redirect_url', '')
        # abs_url = 'http://' + current_site + relative_link
        # email_body = 'Hello,\nUse link below to reset your password\n' + \
        #              abs_url + "?redirect_url=" + redirect_url
        # data = {'email_body': email_body, 'to_email': user.email,
        #         'email_subject': 'Reset your password'}
        # Util.send_email(data)
        # return Response({'message': 'We have sent you a link to reset your password'}, status=HTTP_200_OK)


class PasswordResetAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, uidb64, token):
        utc = pytz.UTC

        try:
            user_data_str = smart_str(urlsafe_base64_decode(uidb64))
            user_id = int(user_data_str.split('||')[0])
            user_email = user_data_str.split('||')[1]
            user = get_object_or_404(UserModel, id=user_id, email=user_email)
            if not user.reset_password_token == token:
                return Response({
                    'message': 'Token does not match, please request a new one',
                }, status=HTTP_400_BAD_REQUEST)

            if not user.reset_password_token_expiry.replace(tzinfo=utc) < datetime.now().replace(tzinfo=utc):
                return Response({
                    'message': 'Token expired, please request a new one',
                }, status=HTTP_400_BAD_REQUEST)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'message': 'Token is not valid, please request a new one',
                }, status=HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            user.set_password(serializer.validated_data['password1'])
            user.reset_password_token = None
            user.reset_password_token_expiry = None
            user.save()

            return Response({
                'message': 'Password reset successfully',
            }, status=HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({
                'message': 'Token is not valid, please request a new one',
            }, status=HTTP_400_BAD_REQUEST)
