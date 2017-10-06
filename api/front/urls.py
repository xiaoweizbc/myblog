# -*- coding: utf-8 -*-
from django.conf.urls import url
import views

urlpatterns = [
    # 第一部分：首页文章列表等
    url(r'^$', views.article_list, name='front_index'),
    url(r'^article_list/(?P<category_id>\d+)/(?P<page>\d+)/$', views.article_list, name='front_article_list'),
    url(r'^article_detail/(?P<article_id>[\w\-]+)/$', views.article_detail, name='front_article_detail'),
    # 第二部分：登录注册登出
    url(r'^signin/$', views.signin, name='front_signin'),
    url(r'^signup/$', views.signup, name='front_signup'),
    url(r'^signout/$', views.signout, name='front_signout'),
    url(r'^forget_password/$', views.forget_password, name='front_forget_password'),
    url(r'^reset_password/(?P<code>\w+)$', views.reset_password, name='front_reset_password'),
    url(r'^check_email/(?P<code>\w+)/$', views.check_email, name='front_check_email'),

    url(r'^comment/$', views.comment, name='front_comment'),

    url(r'^test/$', views.test, name='front_test'),
]
