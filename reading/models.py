# **coding: utf-8**
from __future__ import unicode_literals

from django.db import models


class Book(models.Model):

    BOOK_TYPE_CHOICES = (
        (0, "仙剑"),
        (1, "玄幻"),
        (2, "悬疑"),
        (3, "奇幻"),
        (4, "军事"),
        (5, "历史"),
        (6, "竞技"),
        (7, "科幻"),
        (8, "校园"),
        (9, "社会"),
        (10, "其它"),
    )

    BOOK_STATE_CHOICE = (
        (0, "连载"),
        (1, "完本"),
    )

    author = models.CharField("作者", max_length=6, default="匿名")
    book_name = models.CharField("书名", max_length=15)
    cover = models.ImageField("封面", default="")
    describe = models.TextField("概要", max_length=300)
    type = models.SmallIntegerField("类型", choices=BOOK_TYPE_CHOICES)
    word_number = models.IntegerField("字数", default=0)
    update_state = models.SmallIntegerField("更新状态", default=0)
    chapter_num = models.IntegerField("章节数量", default=0)
    book_money = models.IntegerField("书籍价格", default=0)
    update_time = models.DateTimeField("更新时间", auto_now_add=True)
    isShow = models.BooleanField("是否显示", default=True)
    auditingState = models.BooleanField("审核状态", default=0)

    class Meta:
        db_table = "book"


class BookProfile(models.Model):

    book = models.OneToOneField(Book, primary_key=True)
    click_num = models.IntegerField("点击量", default=0)
    subscriber_num = models.IntegerField("订阅量", default=0)
    chase_book_num = models.IntegerField("追书量", default=0)
    reward_num = models.IntegerField("猫币打赏总数", default=0)
    cat_ball_num = models.IntegerField("猫球打赏总量", default=0)
    catnip_num = models.IntegerField("猫薄荷打赏总量", default=0)
    cat_stick_num = models.IntegerField("逗猫棒打赏总量", default=0)
    cat_food_num = models.IntegerField("猫抓饭打赏总量", default=0)
    cat_fish_num = models.IntegerField("跑爬架打赏总量", default=0)
    cat_house_num = models.IntegerField("猫窝打赏总量", default=0)

    class Meta:
        db_table = "book_profile"
