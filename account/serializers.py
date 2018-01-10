# coding=utf-8
from rest_framework import serializers
from .models import User, UserProfile


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=16)


class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=16)


class UserProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    chase_book = serializers.SerializerMethodField()
    subscribe_book = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('user_name', 'phone', 'avatar', 'user_describe', 'balance', 'recommend_ticket_num',
                  'diamond_ticket_num', 'chase_book', 'subscribe_book')

    def get_user_name(self, obj):
        return obj.user.user_name

    def get_phone(self, obj):
        return obj.user.phone[:3] + '****' + obj.user.phone[-4:]

    def get_chase_book(self, obj):
        return obj.user.userprofile.chase_book

    def get_subscribe_book(self, obj):
        return obj.user.userprofile.subscribe_book
