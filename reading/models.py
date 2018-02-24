# **coding: utf-8**
from __future__ import unicode_literals

from django.db import models
from account.models import User


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

    # 作者
    author = models.CharField(max_length=6, default="匿名")
    # 书名
    book_name = models.CharField(max_length=15)
    # 封面
    cover = models.ImageField(default="")
    # 概要
    book_describe = models.TextField(max_length=300)
    # 书籍类型
    book_type = models.SmallIntegerField(choices=BOOK_TYPE_CHOICES)
    # 字数
    word_number = models.IntegerField(default=0)
    # 更新状态
    update_state = models.SmallIntegerField(default=0)
    # 章节数量
    chapter_num = models.IntegerField(default=0)
    # 书籍价格
    book_money = models.IntegerField(default=0)
    # 更新时间
    update_time = models.DateTimeField(auto_now_add=True)
    # 是否显示
    is_show = models.BooleanField(default=True)
    # 审核状态
    auditing_state = models.BooleanField(default=0)

    class Meta:
        db_table = "book"


class BookProfile(models.Model):
    book = models.OneToOneField(Book, primary_key=True)
    # 书籍评分
    book_rank = models.SmallIntegerField(default=0)
    # 点击量
    click_num = models.IntegerField(default=0)
    # 订阅量
    subscriber_num = models.IntegerField(default=0)
    # 追书量
    chase_book_num = models.IntegerField(default=0)
    # 猫币打赏总数
    reward_num = models.IntegerField(default=0)
    # 猫球打赏总量
    cat_ball_num = models.IntegerField(default=0)
    # 猫薄荷打赏总量
    catnip_num = models.IntegerField(default=0)
    # 逗猫棒打赏总量
    cat_stick_num = models.IntegerField(default=0)
    # 猫抓饭打赏总量
    cat_food_num = models.IntegerField(default=0)
    # 跑爬架打赏总量
    cat_fish_num = models.IntegerField(default=0)
    # 猫窝打赏总量
    cat_house_num = models.IntegerField(default=0)

    class Meta:
        db_table = "book_profile"


class BookChapter(models.Model):

    """
    章节内容
    """

    # 书籍章节类型选项
    CHAPTER_TYPE_CHOICE = (
        (0, "免费"),
        (1, "收费"),
    )

    # 书籍章节状态选项
    CHAPTER_STATE_CHOICE = (
        (0, "不发布"),
        (1, "发布"),
    )

    # 对应的图书ID
    book = models.ForeignKey(Book, related_name='book_chapter')
    # 章节数
    chapter_id = models.SmallIntegerField()
    # 章节名称
    chapter_name = models.CharField(max_length=20)
    # 该章节的内容
    chapter_content = models.TextField()
    # 章节字数
    word_number = models.IntegerField(default=0)
    # 改章节更新时间
    update_date = models.DateTimeField(auto_now_add=True)
    # 章节类型
    chapter_type = models.IntegerField(default=0, choices=CHAPTER_TYPE_CHOICE)
    # 章节状态
    chapter_state = models.IntegerField(default=0, choices=CHAPTER_STATE_CHOICE)
    # 章节价钱
    chapter_money = models.IntegerField(default=0)
    # 章节浏览量
    chapter_PV = models.IntegerField(default=0)

    class Meta:
        db_table = "book_chapter"


class BookComment(models.Model):

    # 书籍更新状态选项
    COMMENT_TYPE_CHOICE = (
        (0, "一般"),
        (1, "精华"),
        (2, "置顶"),
        (3, "精华并置顶"),
    )

    user = models.ForeignKey(User, related_name='book_comment')
    book = models.ForeignKey(Book, related_name='book_comment')
    # 评论类型
    comment_type = models.IntegerField(choices=COMMENT_TYPE_CHOICE, default=0)
    # 评论内容
    comment_content = models.CharField(max_length=120)
    # 评论时间
    comment_date = models.DateTimeField(auto_now_add=True)
    # 评论是否显示
    is_show = models.BooleanField(default=False)

    class Meta:
        db_table = "book_comment"
