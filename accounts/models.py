from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Default custom user.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta(AbstractUser.Meta):
        default_related_name = 'users'

    def __str__(self):
        return self.username
