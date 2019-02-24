from django.db import models

# Create your models here.


class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女')
    )

    name = models.CharField(max_length=128, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    sex = models.CharField(
        max_length=32,
        choices=gender,
        default='男',
        verbose_name = '性别'
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    has_confirmed = models.BooleanField(default=False)  # 邮件是否确认，未进行邮件注册

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    """邮件确认，保存用户注册码之间的关系，一对一"""
    code = models.CharField(max_length=256, verbose_name='确认码')     # 哈希后的注册码
    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name='关联的用户')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')   # 提交时间

    def __str__(self):
        return self.user.name + ': ' + self.code

    class Meta:
        ordering = ['-created_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'
