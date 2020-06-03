from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class UserProfile(AbstractUser):
    date_joined = None
    email = None
    first_name = None
    is_active = None
    is_staff = None
    is_superuser = None
    last_login = None
    last_name = None
    t_open_id = models.PositiveIntegerField(primary_key=False, default=0)
    diamonds =  models.PositiveIntegerField(primary_key=False, default=0)
    
    objects = UserManager()

