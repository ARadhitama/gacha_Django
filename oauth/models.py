from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    t_open_id = models.PositiveIntegerField(primary_key=False, default=0)
    diamonds =  models.PositiveIntegerField(primary_key=False, default=0)
    last_login = None 
    
    USERNAME_FIELD = 'username'
    objects = UserManager()

