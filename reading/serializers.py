# **coding=utf-8**
from .models import Book, BookComment, BookChapter
from rest_framework import serializers


class ListModuleSerializer(serializers.ModelSerializer):

    """"书籍列表序列化"""

    book_type = serializers.SerializerMethodField()
    book_rank = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('book_name', 'id', 'book_type', 'author', 'book_rank')

    def get_book_type(self, obj):
        return Book.BOOK_TYPE_CHOICES[obj.book_type][1]

    def get_book_rank(self, obj):
        return obj.bookprofile.book_rank


class SwiperBookSerializer(serializers.ModelSerializer):

    """滑动书籍序列化"""

    book_rank = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('book_name', 'id', 'author', 'cover', 'book_rank')

    def get_book_rank(self, obj):
        return obj.bookprofile.book_rank


class BookSerializer(serializers.ModelSerializer):

    """书籍基本序列化"""

    book_type = serializers.SerializerMethodField()
    update_state = serializers.SerializerMethodField()
    book_rank = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'word_number', 'book_type', 'book_describe', 'author', 'cover', 'chapter_num', 'book_name',
                  'update_state', 'book_rank')

    def get_book_type(self, obj):
        return Book.BOOK_TYPE_CHOICES[obj.book_type][1]

    def get_update_state(self, obj):
        return Book.BOOK_STATE_CHOICE[obj.update_state][1]

    def get_book_rank(self, obj):
        return obj.bookprofile.book_rank


class BookCommentSerializer(serializers.ModelSerializer):

    """书籍评论序列化"""

    def __init__(self):
        super(BookCommentSerializer, self).__init__()
        self.MONTH = [u'一月', u'二月', u'三月', u'四月', u'五月', u'六月',
                      u'七月', u'八月', u'九月', u'十月', u'十一月', u'十二月']

    user_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    comment_date = serializers.SerializerMethodField()

    class Meta:
        model = BookComment
        fields = ('comment_content', 'comment_date', 'user_name', 'avatar')

    def get_user_name(self, obj):
        return obj.user.user_name

    def get_avatar(self, obj):
        return str(obj.user.userprofile.avatar)

    def get_comment_date(self, obj):
        month = self.MONTH[obj.comment_date.month-1]
        return '{0} {1}, {2}'.format(month, obj.comment_date.day, obj.comment_date.year)


class BookInfoSerializer(serializers.ModelSerializer):

    """书籍详情页序列化"""

    cat_ball_num = serializers.SerializerMethodField()
    catnip_num = serializers.SerializerMethodField()
    cat_stick_num = serializers.SerializerMethodField()
    cat_food_num = serializers.SerializerMethodField()
    cat_fish_num = serializers.SerializerMethodField()
    cat_house_num = serializers.SerializerMethodField()

    book_comment = BookCommentSerializer(many=True)

    book_rank = serializers.SerializerMethodField()
    book_type = serializers.SerializerMethodField()
    update_state = serializers.SerializerMethodField()

    # last_chapter = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'word_number', 'book_type', 'book_describe', 'author', 'cover', 'chapter_num', 'book_name',
                  'update_state', 'cat_ball_num', 'catnip_num', 'catnip_num', 'cat_stick_num', 'cat_food_num',
                  'cat_fish_num', 'cat_house_num', 'book_rank', 'book_comment')

    def get_book_type(self, obj):
        return Book.BOOK_TYPE_CHOICES[obj.book_type][1]

    def get_update_state(self, obj):
        return Book.BOOK_STATE_CHOICE[obj.update_state][1]

    def get_cat_ball_num(self, obj):
        return obj.bookprofile.cat_ball_num

    def get_catnip_num(self, obj):
        return obj.bookprofile.catnip_num

    def get_cat_stick_num(self, obj):
        return obj.bookprofile.cat_stick_num

    def get_cat_food_num(self, obj):
        return obj.bookprofile.cat_food_num

    def get_cat_fish_num(self, obj):
        return obj.bookprofile.cat_fish_num

    def get_cat_house_num(self, obj):
        return obj.bookprofile.cat_house_num

    def get_book_rank(self, obj):
        return obj.bookprofile.book_rank

    # def get_last_chapter(self, obj):
    #     last_chapter = BookChapter.objects.filter(book=obj)[-1]
        # return '第{0}章 {1}'.format(last_chapter.chapter_id, last_chapter.chapter_name)


class BookCatalogSerializer(serializers.ModelSerializer):
    """　书籍目录序列化　"""

    chapter = serializers.SerializerMethodField()

    class Meta:
        model = BookChapter
        fields = ('chapter', 'chapter_id')

    def get_chapter(self, obj):
        return "第{0}章　{1}".format(obj.chapter_id, obj.chapter_name)


class BookChapterSerializer(serializers.ModelSerializer):
    """ 书籍内容序列化 """

    class Meta:
        model = BookChapter
        fields = ('chapter_name', 'chapter_id', 'chapter_content', 'word_number', 'update_date', 'chapter_type',
                  'chapter_money')
