# **coding: utf-8**
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from jsonfield import JSONField


class UserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, phone):
        return self.get(**{self.model.USERNAME_FIELD: phone})

REGULAR_USER = 0
ADMIN = 1


class User(AbstractBaseUser):
    # 用户名
    user_name = models.CharField(max_length=14)
    # 手机号
    phone = models.CharField(max_length=11, unique=True)
    # 用户是否可用
    is_forbidden = models.BooleanField(default=True)
    # 用户注册时间
    register_time = models.DateTimeField(auto_now_add=True)
    # 0代表不是管理员　1是管理员
    admin_type = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    class Meta:
        db_table = "user"


class UserProfile(models.Model):
    # 对应用户
    user = models.OneToOneField(User)
    # 用户头像
    avatar = models.ImageField(default="avatar_default.jpg")
    # 用户简介
    user_describe = models.CharField(max_length=40)
    # 用户类型
    type = models.IntegerField(default=0)
    # 推荐票数量
    recommend_ticket_num = models.IntegerField(default=0)
    # 钻石票数量
    diamond_ticket_num = models.IntegerField(default=0)
    # 猫币余额
    balance = models.IntegerField(default=0)
    # JSON字典用来表示该用户的追书
    chase_book = JSONField(default={})
    # JSON字典用来表示该用户的订阅
    subscriber_book = JSONField(default={})

    class Meta:
        db_table = "user_profile"

    def update_chase_book(self, book_id):
        if str(book_id) in self.chase_book:
            return
        else:
            info = {'add_time': 0, 'is_buy': False}
            self.chase_book[book_id] = info

    def update_subscriber_book(self, book_id):
        if str(book_id) in self.chase_book:
            return
        else:
            info = {'add_time': 0, 'is_buy': False}
            self.chase_book[book_id] = info
