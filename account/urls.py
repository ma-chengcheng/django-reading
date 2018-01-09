# -*- coding: utf-8 -*-
import views
from django.conf.urls import url

urlpatterns = [
    url(r'^UserLoginAPIView/$', views.UserLoginAPIView.as_view()),
    url(r'^UserRegisterAPIView/$', views.UserRegisterAPIView.as_view()),
    url(r'^UserLogoutAPIView/$', views.UserLogoutAPIView.as_view()),
    url(r'^ResetPasswordAPIView/$', views.ResetPasswordAPIView.as_view()),
    url(r'^IsRegisteredAPIView/$', views.IsRegisteredAPIView.as_view()),
    url(r'^SendMessageAPIView/$', views.SendMessageAPIView.as_view()),
    url(r'^CheckVerifyCodeAPIView/$', views.CheckVerifyCodeAPIView.as_view()),
    url(r'^UserIsActiveAPIView/$', views.UserIsActiveAPIView.as_view()),
    url(r'^UserProfileAPIView/$', views.UserProfileAPIView.as_view()),
    url(r'^UploadAvatarAPIView/$', views.UploadAvatarAPIView.as_view()),
    url(r'^SetUserDescribeAPIView/$', views.SetUserDescribeAPIView.as_view()),
    url(r'^SetUserDescribeAPIView/$', views.SetUserDescribeAPIView.as_view()),
]
