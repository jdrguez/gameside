import uuid

from django.conf import settings
from django.db import models


# Create your models here.
class Token(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='token',
        on_delete=models.CASCADE,
    )
    key = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
