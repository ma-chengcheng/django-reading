# **coding: utf-8**
import os
import random
from django.conf import settings
from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserProfileSerializer, UserLoginSerializer, UserRegisterSerializer
from utils.SMSVerification import SMSVerification
from utils.shortcuts import success_response, error_response
from .models import User, UserProfile
from django.views.decorators.csrf import csrf_exempt
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class UserLoginAPIView(APIView):
    """
    用户登录json api接口
    ---
    request_serializer: UserLoginSerializer
    """

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = auth.authenticate(phone=data["phone"], password=data["password"])
            if user:
                auth.login(request, user)
                user_profile = UserProfile.objects.get(user=request.user)
                serializer = UserProfileSerializer(user_profile)
                content = dict()
                content['state'] = 'true'
                content['user_profile'] = serializer.data
                return Response(data=content)
            else:
                return error_response(u"登录失败")
        else:
            return error_response(u"登录失败")


class UserRegisterAPIView(APIView):

    """
    用户注册json api接口
    ———
    request_serializer: UserRegisterSerializer
    """

    @ csrf_exempt
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            print "ok"
            data = serializer.data
            user = User.objects.create(phone=data["phone"])
            user.set_password(data["password"])
            user_name = "用户#" + str(random.randrange(1000, 9000))
            user.user_name = user_name
            user.save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            return success_response('注册成功')
        else:
            return error_response('注册失败')


class ResetPasswordAPIView(APIView):

    """
    密码重置json api接口
    """
    def get(self, request):
        phone = request.GET.get("phone")
        password = request.GET.get("password")
        user = User.objects.get(phone=phone)
        user.set_password(password)
        user.save()
        return success_response('修改成功')


class UserLogoutAPIView(APIView):

    def get(self, request):
        auth.logout(request)
        message = u"成功退出"
        return success_response(message)


class IsRegisteredAPIView(APIView):

    """
    用户是否注册json api接口
    """

    def get(self, request):
        phone = request.GET.get("phone")
        is_registered = 'true'
        try:
            User.objects.get(phone=phone)
        except User.DoesNotExist:
            is_registered = 'false'
        return Response(data={"is_registered": is_registered})


class SendMessageAPIView(APIView):

    """
    发送验证json api接口
    """

    def get(self, request):
        phone = str(request.GET.get("phone"))
        # 生成并保存验证码
        verify_code = repr(random.randint(1000, 9999))
        request.session['verify_code'] = verify_code

        sms_verification = SMSVerification(str(phone), verify_code)
        sms_verification.send_verify_code()
        return success_response('短信发送成功')


class CheckVerifyCodeAPIView(APIView):

    """
    检查验证马json api接口
    """

    def get(self, request):
        verify_code = request.GET.get("verifyCode")
        print verify_code
        print request.session.get('verify_code')
        if verify_code == request.session.get('verify_code'):
            return success_response('验证通过')
        else:
            return error_response('验证码有误')


class UserIsActiveAPIView(APIView):

    """
    用户是否登录
    """

    def get(self, request):
        if request.user.is_authenticated():
            return success_response("已登录")
        else:
            return error_response("未登录")


class UserProfileAPIView(APIView):

    """
    获取用户信息　json api接口
    """

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        content = dict()
        content['state'] = 'true'
        content['user_profile'] = serializer.data
        content['user_is_active'] = 'true'
        return Response(data=content)


class UploadAvatarAPIView(APIView):

    """
    上传用户头像
    """

    @ csrf_exempt
    def post(self, request):
        if "file" not in request.FILES:
            return error_response('图片上传失败')
        else:
            avatar = request.FILES['file']
            avatar_name = "avatar_" + os.path.splitext(avatar.name)[-1]
            with open(os.path.join(settings.AVATAR_UPLOAD_DIR, avatar_name), "wb") as avatar:
                for chunk in request.FILES['file']:
                    avatar.write(chunk)
            return success_response('图片上传成功')


class SetUserName(APIView):

    """
    重置用户名
    """

    def get(self, request):
        user = request.user
        new_user_name = request.GET.get('new_user_name')
        user.user_name = new_user_name
        user.save()
        return success_response('修改成功')


class SetUserDescribeAPIView(APIView):

    """
    设置用户签名
    """
    def post(self, request):
        user_describe = request.data['new_user_describe']
        user_profile = request.user.userprofile
        user_profile.user_describe = user_describe
        user_profile.save()
        return success_response('修改成功')


class SetPhoneAPIView(APIView):

    """
    设置手机
    """

    def get(self, request):
        user = request.user
        new_phone = request.GET.get('new_phone')
        user.phone = new_phone
        user.save()
        return success_response('修改成功')
