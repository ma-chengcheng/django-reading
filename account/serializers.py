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

    class Meta:
        model = UserProfile
        fields = ('user_name', 'phone', 'avatar', 'user_describe', 'balance', 'recommend_ticket_num', 'diamond_ticket_num')

    def get_user_name(self, obj):
        return obj.user.user_name

    def get_phone(self, obj):
        return obj.user.phone[:3] + '****' + obj.user.phone[-4:]

