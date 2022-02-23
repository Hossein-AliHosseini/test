from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        permissions = [
            ('read_index', "Can view all indexes"),
            ('delete_index', "Can delete any index"),
            ('create_index', "Can create a new index"),
            ('update_index', "Can update any existing index"),
        ]

    def __str__(self):
        return self.email
