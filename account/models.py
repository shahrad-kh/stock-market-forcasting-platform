from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Add any additional fields if needed.
    """
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'


    def __str__(self):
        return self.username

