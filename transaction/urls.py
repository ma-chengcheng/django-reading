# -*- coding: utf-8 -*-
import views
from django.conf.urls import url

urlpatterns = [
    url(r'^PayAPIView/$', views.PayAPIView.as_view()),
]
