from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from common.admin import RawIdFieldsAdmin
from .models import UserModel


@admin.register(UserModel)
class UserModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = (
        'username',
        'is_admin', 'is_staff', 'is_superuser',
    )
    list_filter = ('is_admin', 'is_staff', 'is_superuser', 'is_active', 'is_deleted')
    search_fields = ('username',)
    readonly_fields = (
        'password',
        'created_at', 'updated_at',
    )
    fieldsets = (
        (None, {'fields': (
            'username',
            'password',
        )}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser',)}),
    )
