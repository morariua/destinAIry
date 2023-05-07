from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

CustomUser._meta.get_field('groups').related_name = 'customuser_set'
CustomUser._meta.get_field('user_permissions').related_name = 'customuser_set'
CustomUser._meta.get_field('user_permissions').verbose_name = 'permissions'