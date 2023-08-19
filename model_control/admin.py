from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from common.admin import RawIdFieldsAdmin
from .models import ProjectModel, DatasetModel, ColumnModel, TrainModel


@admin.register(ProjectModel)
class ProjectModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = (
        'user',
        'name',
        'description',
    )
    list_filter = ('user', 'is_active', 'is_deleted')
    search_fields = ('name',)
    readonly_fields = (
        'created_at', 'updated_at',
    )
    fieldsets = (
        (None, {'fields': (
            'user',
            'name',
            'description',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_deleted',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(DatasetModel)
class DatasetModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = (
        'name',
        'description',
        'dataset',
        'dataset_size',
        'project_model',
    )
    list_filter = ('project_model', 'is_active', 'is_deleted')
    search_fields = ('name',)
    readonly_fields = (
        'created_at', 'updated_at',
    )
    fieldsets = (
        (None, {'fields': (
            'name',
            'description',
            'dataset',
            'project_model',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_deleted',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(ColumnModel)
class ColumnModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = (
        'name',
        'dataset_model',
        'encoding_type',
        'scaling_type',
        'is_numeric',
        'is_feature',
        'is_target',
    )
    list_filter = ('dataset_model',)
    search_fields = ('name',)
    readonly_fields = (
        'created_at', 'updated_at',
    )
    fieldsets = (
        (None, {'fields': (
            'name',
            'description',
            'dataset_model',
            'encoding_type',
            'scaling_type',
            'is_numeric',
            'is_feature',
            'is_target',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_deleted',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(TrainModel)
class TrainModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = (
        'name',
        'description',
        'project_model',
        'dataset_model',
        'test_size',
        'is_complete',
    )
    list_filter = ('project_model', 'dataset_model',)
    search_fields = ('name',)
    readonly_fields = (
        'created_at', 'updated_at',
    )
    fieldsets = (
        (None,
         {'fields': (
             'name',
             'description',
             'project_model',
             'dataset_model',
             'test_size',
             'model',
             'hyperparameters',
             'metrics',
             'plots',
             'is_training',
             'is_complete',
         )},
         ),
        ('Permissions', {'fields': ('is_active', 'is_deleted',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
