# **coding: utf-8**
import json
import datetime
from rest_framework.views import APIView, Response
from .models import Book, BookComment, BookChapter
from django.db.models import Q
from .serializers import (
    ListModuleSerializer,
    SwiperBookSerializer,
    BookSerializer,
    BookInfoSerializer,
    BookCatalogSerializer,
    BookChapterSerializer
)
from django.core.paginator import Paginator
from utils.shortcuts import error_response
from utils.redis_cache.redis_db import redis_client


class RankBookAPIView(APIView):

    """
    排行榜列表接口
    """

    def __init__(self):
        super(APIView, self).__init__()
        self.RANK_NAME = ['click_rank', 'chase_rank', 'reward_rank', 'new_book_rank', 'subscriber_rank']

    def get(self, request):
        content = dict()
        for rank_name in self.RANK_NAME:
            content[rank_name] = self.get_rank(rank_name)
        return Response(content)

    @ staticmethod
    def get_rank(rank_name):
        book = Book.objects.all()
        if 'click_rank' == rank_name:
            book = book.order_by('-bookprofile__click_num')
        elif 'chase_rank' == rank_name:
            book = book.order_by('-bookprofile__chase_book_num')
        elif 'reward_rank' == rank_name:
            book = book.order_by('-bookprofile__reward_num')
        elif 'new_book_rank' == rank_name:
            book = book.order_by('-update_time')
        elif 'subscriber_rank' == rank_name:
            book = book.order_by('-bookprofile__subscriber_num')
        book = book[:10]
        serializer = SwiperBookSerializer(book, many=True)
        content = dict()
        content['book_items'] = serializer.data
        return content


class IndexBookAPIView(APIView):

    def __init__(self):
        super(APIView, self).__init__()
        self.MODULE_NAME = ['new_book', 'free_book', 'superme_book', 'hot_book']

    def get(self, request):
        content = dict()

        # 未缓存情况
        if redis_client().get('recommend_book') == 'None':
            content['recommend_book'] = self.get_swiper_book()
            redis_client().set('recommend_book', json.dumps(content['recommend_book']))
        else:
            content['recommend_book'] = json.loads(redis_client().get('recommend_book'))

        for module_name in self.MODULE_NAME:

            if redis_client().get(module_name) == 'None':
                content[module_name] = self.get_list(module_name)
                redis_client().set(module_name, json.dumps(content[module_name]))
            else:
                content[module_name] = json.loads(redis_client().get(module_name))

        return Response(data=content)

    @ staticmethod
    def get_list(module_name):
        books = Book.objects.all()
        if 'new_book' == module_name:
            books = books.order_by('-update_time')
        elif 'free_book' == module_name:
            books = books.filter(book_money=0)
        elif 'superme_book' == module_name:
            books = books.order_by('-bookprofile__reward_num')
        elif 'hot_book' == module_name:
            books = books.order_by('-bookprofile__click_num')

        book = books[0]
        book_items = books[1:6]
        serializer = ListModuleSerializer(book_items, many=True)
        top_book = dict()
        top_book['id'] = book.id
        top_book['cover'] = str(book.cover)
        top_book['book_name'] = book.book_name
        top_book['describe'] = book.book_describe
        top_book['author'] = book.author
        top_book['book_type'] = Book.BOOK_TYPE_CHOICES[book.book_type][1]
        top_book['book_rank'] = book.bookprofile.book_rank

        content = dict()
        content['top_book'] = top_book
        content['book_items'] = serializer.data
        return content

    @ staticmethod
    def get_swiper_book():
        book = Book.objects.all()[:7]
        serializer = SwiperBookSerializer(book, many=True)
        content = dict()
        content['book_items'] = serializer.data
        return content


class LibraryBookViewAPI(APIView):

    """
    书库书籍接口
    """

    def get(self, request):
        num_page = request.GET.get("numPage")
        book_type = request.GET.get("book_type")

        normal = request.GET.get("normal")
        is_free = request.GET.get("is_free")
        update_state = request.GET.get("update_state")
        update_date = request.GET.get("update_date")

        book = Book.objects.all()

        # normal筛选
        if 'favorite' == normal:
            book = book.order_by('-bookprofile__click_num')
        elif 'date' == normal:
            book = book.order_by('-update_time')
        elif 'word_number' == normal:
            book = book.order_by('-bookprofile__reward_num')
        elif 'subscribe' == normal:
            book = book.order_by('-bookprofile__subscriber_num')

        # 书籍类型筛选
        if book_type:
            book = book.filter(book_type=book_type)

        # 是否免费筛选
        if '0' == is_free:
            book = book.filter(book_money=0)
        elif '1' == is_free:
            book = book.filter(book_money__gt=0)
        else:
            pass

        # 书籍更新状态筛选
        if '0' == update_state:
            book = book.filter(update_state=0)
        elif '1' == update_state:
            book = book.filter(update_state=1)
        else:
            pass

        # 书籍更新时间筛选
        end_time = datetime.datetime.now()
        if '0' == update_date:
            start_time = (end_time - datetime.timedelta(days=3))
            book = book.filter(update_date__range=(start_time, end_time))
        elif '1' == update_date:
            start_time = (end_time - datetime.timedelta(days=7))
            book = book.filter(update_date__range=(start_time, end_time))
        elif '2' == update_date:
            start_time = (end_time - datetime.timedelta(days=15))
            book = book.filter(update_date__range=(start_time, end_time))
        elif '3' == update_date:
            start_time = (end_time - datetime.timedelta(days=30))
            book = book.filter(update_date__range=(start_time, end_time))
        else:
            pass

        paginator = Paginator(book, 5)
        num_pages = paginator.num_pages
        if num_pages != 0:
            serializers = BookSerializer(paginator.page(num_page).object_list, many=True)
            content = dict()
            content['book_items'] = serializers.data
            content['page_num'] = num_pages
            return Response(data=content)
        else:
            return error_response(u"未筛选到，请重新筛选")


class SearchBookAPIView(APIView):
    """
    搜索书籍接口
    """

    def get(self, request):
        key_value = request.GET.get("key_value")
        content = dict()

        if key_value != '':
            book = Book.objects.filter(Q(book_name__contains=key_value) | Q(author__contains=key_value)).all()
            paginator = Paginator(book, 10)
            serializers = BookSerializer(paginator.page(1).object_list, many=True)
            content['book_items'] = serializers.data
            return Response(data=content)
        else:
            content['book_items'] = None
            return Response(data=content)


class BookInfoAPIView(APIView):
    """
    书籍详情页
    """
    def get(self, request):
        book_id = request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        serializer = BookInfoSerializer(book)
        content = dict()
        content['book_info'] = serializer.data
        return Response(data=content)


class BookCatalogAPIView(APIView):
    """
    书籍目录
    """
    def get(self, request):
        book_id = request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        book_chapter = BookChapter.objects.filter(book=book).all()
        serializer = BookCatalogSerializer(book_chapter, many=True)
        content = dict()
        content['catalog_items'] = serializer.data
        return Response(data=content)


class BookChapterAPIView(APIView):
    """
    书籍章节内容
    """
    def get(self, request):
        book_id = request.GET.get('book_id')
        chapter_id = request.GET.get('chapter_id')
        chapter = BookChapter.objects.filter(book=book_id, chapter_id=chapter_id).get()
        serializer = BookChapterSerializer(chapter)
        return Response(serializer.data)
