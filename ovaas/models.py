from utils.ovaas_user import MyAbstractBaseUser, MyUserManager
from django.contrib.auth.hashers import make_password
from django.db import models, transaction
from db.base_model import BaseModel


class UserManager(MyUserManager):
    def _create_user(self, username, password, **kwargs):

        if not username:
            raise ValueError('The given username must be set')
        try:

            user = User(username=username, **kwargs)
            user.password = make_password(password)
            user.save(using=self._db)
            return user
        except Exception as e:
            print(f"error is :{e}")

    def create_user(self, username, password, **kwargs):
        return self._create_user(username, password, **kwargs)


class User(MyAbstractBaseUser):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=50, verbose_name='user', unique=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        db_table = 'UserInfo'
        verbose_name = 'User'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id
