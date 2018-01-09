# **coding: utf-8**
from rest_framework.response import Response


def success_response(data):
    return Response(data={"state": 'true', "message": data})


def error_response(data):
    return Response(data={"state": 'false', "message": data})
