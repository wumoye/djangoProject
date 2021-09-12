from django.db import models


class BaseModel(models.Model):

    class Meta:
        abstract = True

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='createtime')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='updatetime')
    is_delete = models.BooleanField(default=False, verbose_name='isdelete')
