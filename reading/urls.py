# -*- coding: utf-8 -*-
import views
from django.conf.urls import url

urlpatterns = [
    url(r'^RankBookAPIView/$', views.RankBookAPIView.as_view()),
    # url(r'^ListModuleViewAPI/$', views.ListModuleViewAPI.as_view()),
    # url(r'^SwiperModuleViewAPI/$', views.SwiperModuleViewAPI.as_view()),
    url(r'^LibraryBookViewAPI/$', views.LibraryBookViewAPI.as_view()),
    url(r'^SearchBookAPIView/$', views.SearchBookAPIView.as_view()),
    url(r'^BookInfoAPIView/$', views.BookInfoAPIView.as_view()),

    url(r'^IndexBookAPIView/$', views.IndexBookAPIView.as_view()),
    url(r'^BookCatalogAPIView/$', views.BookCatalogAPIView.as_view()),
]
