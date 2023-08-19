from django.db import models
from django.db.models.deletion import RestrictedError


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except RestrictedError as e:
            warning_message = '[Cannot delete]'
            raise RestrictedError(warning_message, e.restricted_objects)
