# **coding=utf-8**
from rest_framework import serializers
from .models import Book


class ListModuleSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('book_name', 'id', 'type', 'author')

    def get_type(self, obj):
        return Book.BOOK_TYPE_CHOICES[obj.type][1]


class SwiperBookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    cover = serializers.ImageField(read_only=True)
    book_name = serializers.CharField(read_only=True)
    author = serializers.CharField(read_only=True)


class BookSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    update_state = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'word_number', 'type', 'describe', 'author', 'cover', 'chapter_num', 'book_name', 'update_state')

    def get_type(self, obj):
        return Book.BOOK_TYPE_CHOICES[obj.type][1]

    def get_update_state(self, obj):
        return Book.BOOK_STATE_CHOICE[obj.update_state][1]
