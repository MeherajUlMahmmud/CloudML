from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from common.admin import RawIdFieldsAdmin
from .models import UserModel


@admin.register(UserModel)
class UserModelAdmin(ImportExportModelAdmin, RawIdFieldsAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'country', 'is_staff', 'is_admin', 'is_superuser',
    )
    list_filter = (
        'country', 'is_staff', 'is_admin', 'is_superuser',
    )
    search_fields = (
        'email',
    )
    readonly_fields = (
        'password',
        'reset_password_token',
        'reset_password_token_expiry',
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'first_name', 'last_name',
            'profile_picture', 'phone_number', 'country',
            'otp', 'otp_expiry',
            'password', 'reset_password_token', 'reset_password_token_expiry',
            'groups', 'user_permissions',
        )}),
        ('Permissions', {'fields': (
            'is_staff', 'is_admin', 'is_superuser',
        )}),
        ('Status', {'fields': ('is_active', 'is_deleted')}),
        ('History', {'fields': (
            'created_at', 'updated_at', 'created_by', 'updated_by',
        )}),
    )

    actions = ['reset_password']

    def reset_password(self, request, queryset):
        for user in queryset:
            user.reset_password()
        self.message_user(request, 'Password reset successfully')

    reset_password.short_description = 'Reset Password'
