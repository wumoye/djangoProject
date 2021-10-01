from datetime import datetime, timedelta

import jwt
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import UserManager

from utils.ovaas_user import ReAbstractBaseUser
from django.db import models


class MyUserManager(UserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):

        if not username:
            raise ValueError('The given username must be set')
        try:
            GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
            username = GlobalUserModel.normalize_username(username)
            user = self.model(username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except Exception as e:
            print(f"error is :{e}")


class User(ReAbstractBaseUser):
    username = models.CharField(max_length=16, unique=True)

    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    @property
    def token(self):
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'data': {
                'username': self.username
            }
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.encode('utf-8').decode('utf-8')

    class Meta:
        db_table = 'userinfo'
        verbose_name = 'User'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
