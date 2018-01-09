# **coding: utf-8 **
import functools

# from django.http import HttpResponseRedirect
from .models import ADMIN
from utils.shortcuts import success_response, error_response


class BasePermissionDecorator(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return functools.partial(self.__call__, obj)

    def __call__(self, *args, **kwargs):
        if len(args) == 2:
            self.request = args[1]
        else:
            self.request = args[0]

        if self.check_permission():
            if self.request.user.is_forbidden is True:
                message = '你已被禁用，请与管理员进行联系'
                return error_response(message)
            else:
                return self.func(*args, **kwargs)
        else:
            if self.request.is_ajax():
                message = "可用"
                return　success_response(message)
            else:
                # return HttpResponseRedirect()
                message = '请登录后操作'
                return error_response(message)

    def check_permission(self):
        raise NotImplementedError()


class LoginRequired(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated()


class AdminRequired(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated() and self.request.user.admin_type == ADMIN
