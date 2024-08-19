from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# class User(models.Model):
#     username = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=20)
#     mobile = models.CharField(max_length=11, unique=True)

class User(AbstractUser):
    # 定义数字枚举
    ENUM_CHOICES = (
        (0, 'Option 0'),
        (1, 'Option 1'),
    )
    mobile = models.CharField(max_length=11, unique=True)
    state = models.IntegerField(choices=ENUM_CHOICES, default=0)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
