import logging
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from common.models import BaseModel
from user_control.utils import Util

logger = logging.getLogger(__name__)


class CountryModel(BaseModel):
    # India, Australia, England, etc.
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "country"
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class MyUserManager(BaseUserManager):

    def create_user(self, email, first_name=None, last_name=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name=None, last_name=None, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_verified = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_verified = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(
        CountryModel, related_name='user_country',
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    reset_password_token = models.CharField(
        max_length=255, null=True, blank=True,
        help_text='This token is used to reset the password',
    )
    reset_password_token_expiry = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'

        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def reset_password(self):
        self.set_password("111222")
        self.save()

    def update_last_login(self):
        """
        Updates the last login time for the user.

        """

        logger.info(f"Updating last login time for user: {self.email}")
        try:
            current_time = datetime.now()
            logger.info(f"Current time: {current_time}")
            self.last_login = current_time
            self.save()
        except Exception as e:
            logger.error(f"Error updating last login time: {e}")

    def update_user_country(self, request):
        """
        Updates the user's country based on their IP address if not already set.

        :param request: HTTP request object.
        """

        logger.info(f"Updating user country for user: {self.email}")
        try:
            if self.country is None and request is not None:
                logger.info(f"User country is not set. Updating user country.")
                ip_address = Util.get_client_ip(request)
                logger.info(f"User IP address: {ip_address}")
                country_code = Util.get_country_from_ip(ip_address)
                logger.info(f"User country code: {country_code}")
                country = CountryModel.objects.filter(code=country_code).first()
                logger.info(f"User country: {country}")
                if country:
                    self.country = country
                    self.save()
                    logger.info(f"User country updated successfully.")

            logger.info(f"User country already set.")
        except Exception as e:
            logger.error(f"Error updating user country: {e}")

    def update_profile_picture(self, profile_picture):
        """
        Updates the user's profile picture.

        :param profile_picture: Profile picture URL.
        """

        logger.info(f"Updating profile picture for user: {self.email}")
        try:
            self.profile_picture = profile_picture
            self.save()
            logger.info(f"Profile picture updated successfully.")
        except Exception as e:
            logger.error(f"Error updating profile picture: {e}")

    def tokens(self):
        tokens = RefreshToken.for_user(self)
        return {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }

    @staticmethod
    def check_object_permissions(request, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        if request.user == obj.created_by:
            return True
        return False

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
