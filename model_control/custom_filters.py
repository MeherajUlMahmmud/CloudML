from django_filters.rest_framework import FilterSet, DateFromToRangeFilter, BooleanFilter
from django_filters.rest_framework import FilterSet, DateFromToRangeFilter, BooleanFilter
from django_filters.widgets import BooleanWidget

from common.custom_widgets import CustomDateRangeFilterWidget, CustomTextField
from model_control.models import ColumnModel, TrainModel


class ColumnModelFilter(FilterSet):
    dataset_model = BooleanFilter(
        field_name="dataset_model", label="Dataset ID",
        widget=CustomTextField(attrs={'placeholder': 'Dataset ID'}),
    )
    is_numeric = BooleanFilter(
        field_name="is_numeric", label="Is Numeric",
        widget=BooleanWidget(attrs={'class': 'form-check-input'})
    )
    is_feature = BooleanFilter(
        field_name="is_feature", label="Is Feature",
        widget=BooleanWidget(attrs={'class': 'form-check-input'})
    )
    is_target = BooleanFilter(
        field_name="is_target", label="Is Target",
        widget=BooleanWidget(attrs={'class': 'form-check-input'})
    )
    created_at = DateFromToRangeFilter(
        field_name="created_at", label="Created At",
        widget=CustomDateRangeFilterWidget(attrs={'placeholder': 'YYYY-MM-DD'}),
    )

    class Meta:
        model = ColumnModel
        fields = [
            'dataset_model',
            'is_numeric',
            'is_feature',
            'is_target',
            'created_at',
        ]


class TrainModelFilter(FilterSet):
    dataset_model = BooleanFilter(
        field_name="dataset_model", label="Dataset ID",
        widget=CustomTextField(attrs={'placeholder': 'Dataset ID'}),
    )
    project_model = BooleanFilter(
        field_name="project_model", label="Project ID",
        widget=CustomTextField(attrs={'placeholder': 'Project ID'}),
    )
    is_training = BooleanFilter(
        field_name="is_training", label="Is Training",
        widget=BooleanWidget(attrs={'class': 'form-check-input'})
    )
    is_complete = BooleanFilter(
        field_name="is_complete", label="Is Complete",
        widget=BooleanWidget(attrs={'class': 'form-check-input'})
    )
    created_at = DateFromToRangeFilter(
        field_name="created_at", label="Created At",
        widget=CustomDateRangeFilterWidget(attrs={'placeholder': 'YYYY-MM-DD'}),
    )

    class Meta:
        model = TrainModel
        fields = [
            'dataset_model',
            'project_model',
            'is_training',
            'is_complete',
            'created_at',
        ]
