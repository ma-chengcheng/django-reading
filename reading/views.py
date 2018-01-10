# **coding: utf-8**
from rest_framework.views import APIView, Response
from .models import Book
from django.db.models import Q
from .serializers import (
    ListModuleSerializer,
    SwiperBookSerializer,
    BookSerializer
)
from django.core.paginator import Paginator


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
        self.MODULE_NAME = ['newBook', 'free_book', 'superme_book', 'hot_book']

    def get(self, request):
        content = dict()
        content['recommend_book'] = self.get_swiper_book()
        for module_name in self.MODULE_NAME:
            content[module_name] = self.get_list(module_name)
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
        top_book['describe'] = book.describe
        top_book['author'] = book.author
        top_book['type'] = Book.BOOK_TYPE_CHOICES[book.type][1]

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
        book = Book.objects.all()
        paginator = Paginator(book, 5)
        num_pages = paginator.num_pages
        serializers = BookSerializer(paginator.page(num_page).object_list, many=True)
        content = dict()
        content['book_items'] = serializers.data
        content['page_num'] = num_pages
        return Response(data=content)


class SearchBookAPIView(APIView):
    """
    搜索书籍接口
    """

    def get(self, request):
        key_value = request.GET.get("key_value")
        content = dict()

        print key_value

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
        serializer = BookSerializer(book)
        content = dict()
        content['book_info'] = serializer.data
        return Response(data=content)

