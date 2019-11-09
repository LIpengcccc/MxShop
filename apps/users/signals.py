# encoding: utf-8
"""
@author:lipeng
@time:2019/10/23  16:50
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

User = get_user_model()

# 加了装饰器自动返回了
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()

