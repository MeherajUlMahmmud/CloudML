from django.forms import Select
from django_filters.rest_framework import (
    FilterSet, BooleanFilter, DateFromToRangeFilter,
)

from common.choices import YesNoChoices
from common.custom_widgets import CustomDateRangeFilterWidget
from user_control.models import UserModel


class UserModelFilter(FilterSet):
    is_verified = BooleanFilter(
        field_name="is_verified", label="Is Verified",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        ),
    )
    is_staff = BooleanFilter(
        field_name="is_staff", label="Is Staff",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        ),
    )
    is_admin = BooleanFilter(
        field_name="is_admin", label="Is Admin",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        ),
    )
    is_superuser = BooleanFilter(
        field_name="is_superuser", label="Is Superuser",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        ),
    )
    is_active = BooleanFilter(
        field_name="is_active", label="Is Active",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        ),
    )
    is_deleted = BooleanFilter(
        field_name="is_deleted", label="Is Deleted",
        widget=Select(
            attrs={'class': 'form-control'},
            choices=YesNoChoices,
        ),
    )
    created_at = DateFromToRangeFilter(
        field_name="created_at", label="Created At",
        widget=CustomDateRangeFilterWidget(),
    )

    class Meta:
        model = UserModel
        fields = [
            'is_verified',
            'is_staff',
            'is_admin',
            'is_superuser',
            'is_active',
            'is_deleted',
            'created_at',
        ]
