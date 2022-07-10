from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    '''自定义用户模型类'''
    mobile=models.CharField(max_length=11,unique=True,verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_user'  # 自定义数据库表名为tb_user
        verbose_name = '用户'  # 后台显示用户表
        verbose_name_plural = '用户表'

    # 调试用的
    def __str__(self):
        return self.username