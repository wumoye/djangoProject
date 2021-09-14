from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from db.base_model import BaseModel


class User(AbstractUser,BaseModel):

    class Meta:
        db_table = 'UserInfo'
        verbose_name = 'user'
        verbose_name_plural = verbose_name