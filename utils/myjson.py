# -*- coding: utf-8 -*-
from django.http import JsonResponse
from collections import namedtuple
"""
http状态码:
200: 请求正常(ok)
400: 请求参数错误(paramserror)
401: 没有权限访问(unauth)
405: 请求方法错误(methoderror)
"""
HttpCode = namedtuple('HttpCode', ['ok', "paramserror", 'unauth', 'methoderror'])  # 定义一个namedtuple类型HttpCode，并包含ok，paramserror，unauth和methoderror属性。
httpcode = HttpCode(ok=200, paramserror=400, unauth=401, methoderror=405)  # 创建一个HttpCode对象
# httpcode = HttpCode._make([200, 400, 401, 405])  # 也可以通过一个list来创建一个User对象，这里注意需要使用"_make"方法


# 请求正常的json返回函数
def json_result(code=httpcode.ok, message='', data={}, kwargs={}):
    json = {
        'code': code,
        'message': message,
        'data': data
    }
    if kwargs.keys():
        # 把json和kwargs合并成一个字典
        for k, v in kwargs.items():
            json[k] = v
    return JsonResponse(json)


def json_params_error(message=''):  # 请求参数错误
    return json_result(code=httpcode.paramserror, message=message)


def json_unauth_error(message=''):  # 没有权限访问
    return json_result(code=httpcode.unauth, message=message)


def json_method_error(message=''):  # 请求方法错误
    return json_result(code=httpcode.methoderror, message=message)
