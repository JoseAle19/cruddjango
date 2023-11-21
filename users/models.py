from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.EmailField(unique=True)
    last_name = models.EmailField(unique=True, default="")
    username = models.CharField(unique=True, max_length=30)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    active_account = models.BooleanField(default=True)
    password = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'user'
