# -*- coding: utf-8 -*-
from django.shortcuts import render, reverse
from django.http import HttpResponse
from models import FrontUserModel
from utils import login, logout
import configs
from decorators import front_login_required


def add_user(request):
    user = FrontUserModel(email='ccc@qq.com', username='ccc', password='123')
    user.save()
    return HttpResponse('success')


def test(request):
    # 从数据库中查找用户，然后密码也要相匹配
    email = 'xiaoweizbc@163.com'
    password = '123456'
    user = FrontUserModel.objects.filter(email=email).first()
    user.set_password('123')
    # if user.check_password(password):
    # 	return HttpResponse(u'验证成功')
    # else:
    # 	return HttpResponse(u'验证失败')

    return HttpResponse(u'success')

# 登录
def front_login(request):
    email = 'xiaoweizbc@163.com'
    password = '123456'
    user = login(request, email, password)
    print user  # 登录成功：FrontUserModel object

    if user:
        print user.email
        print user.username
        return HttpResponse(u'%s%s\n登录成功')
    else:
        return HttpResponse(u'登录失败')

# 检测是否登录
def check_login(request):
    uid = request.session.get(configs.LOGINED_KEY)
    user = FrontUserModel.objects.filter(pk=uid).first()
    print user  #
    if user:
        print "已登录用户信息如下："
        print user.email
        print user.username
        return HttpResponse(u'验证成功\n已登录用户信息如下：\n%s%s'%(user.email, user.username))
    else:
        return HttpResponse(u'验证失败\n没有用户登录')


def front_logout(request):
    logout(request)
    return HttpResponse(u'退出成功')


@front_login_required
def decorator_check(request):
    print '-' * 30
    print reverse('front_signin') + '?next=' + request.path
    print '-' * 30
    return HttpResponse(u'您在已经登录的情况下访问了本页面')


def middleware_test(request):
    if not hasattr(request, 'front_user'):
        return HttpResponse(u'失败')
    else:
        return HttpResponse('成功')
