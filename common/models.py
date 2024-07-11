from django.db import models
from django.db.models.deletion import RestrictedError


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'user_control.UserModel', related_name='%(class)s_created_by',
        on_delete=models.SET_NULL, null=True, blank=True,
    )
    updated_by = models.ForeignKey(
        'user_control.UserModel', related_name='%(class)s_updated_by',
        on_delete=models.SET_NULL, null=True, blank=True,
    )

    objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except RestrictedError as e:
            warning_message = '[Cannot delete]'
            raise RestrictedError(warning_message, e.restricted_objects)


class ContactUsModel(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    is_checked = models.BooleanField(default=False)

    class Meta:
        db_table = 'contact_us'
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.name


class RequestLog(models.Model):
    user = models.ForeignKey(
        'user_control.UserModel', on_delete=models.CASCADE,
        null=True, blank=True,
    )
    ip_address = models.GenericIPAddressField()
    endpoint = models.CharField(max_length=255)
    status_code = models.IntegerField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_name = self.user.get_full_name() if self.user else 'Anonymous'
        return f"{user_name} - {self.endpoint} - {self.created_at}"
