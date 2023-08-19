from django.forms import Select
from django_filters import CharFilter, ChoiceFilter
from django_filters.rest_framework import FilterSet, DateFromToRangeFilter, BooleanFilter
from django_filters.widgets import BooleanWidget

from common.custom_widgets import CustomDateRangeFilterWidget, CustomNumberField, CustomTextField
from user_control.models import UserModel


class UserModelFilter(FilterSet):
    is_superuser = BooleanFilter(
        field_name="is_superuser", label="Is Superuser",
        widget=BooleanWidget(attrs={'class': 'form-check-input'})
    )
    created_at = DateFromToRangeFilter(
        field_name="created_at", label="Created At",
        widget=CustomDateRangeFilterWidget(attrs={'placeholder': 'YYYY-MM-DD'}),
    )

    class Meta:
        model = UserModel
        fields = [
            'is_superuser',
            'created_at',
        ]
