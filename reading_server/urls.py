# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.conf.urls import url
from django.contrib import admin

import account
import utils
import reading
import transaction
from account import urls
from utils import urls
from reading import urls
from transaction import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(account.urls), name='account_URLConf'),
    url(r'^', include(reading.urls), name='reading_URLConf'),
    url(r'^', include(utils.urls), name='utils_URLConf'),
    url(r'^', include(transaction.urls), name='transaction_URLConf'),
]
