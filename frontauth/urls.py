# -*- coding: utf-8 -*-
from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^front_login/$', views.front_login),  # 测试前台登录：http://127.0.0.1:8000/auth/front_login/
    url(r'^front_logout/$', views.front_logout),  # 测试前台登出：http://127.0.0.1:8000/auth/front_login/
    url(r'^check_login/$', views.check_login),
    url(r'^add_user/$', views.add_user),
    url(r'^test/$', views.test),
    url(r'^decorator_check/$', views.decorator_check),
    url(r'^middleware_test/$', views.middleware_test),
]
