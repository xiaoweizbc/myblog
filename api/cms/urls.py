# -*- coding: utf-8 -*-
from django.conf.urls import url
import views

urlpatterns = [
    # 第零部分：主页
    url(r'^$', views.article_manage, name='cms_index'),
    # 第一部分：登入登出
    url(r'^login/$', views.cms_login, name='cms_login'),
    url(r'^logout/$', views.cms_logout, name='cms_logout'),
    # 第二部分：个人设置等
    url(r'^settings/$', views.cms_settings, name='cms_settings'),
    url(r'^update_profile/$', views.update_profile, name='cms_update_profile'),
    url(r'^get_token/$', views.get_token, name='cms_get_token'),
    url(r'^update_email/$', views.update_email, name='cms_update_email'),
    url(r'^check_email/(?P<code>\w+)$', views.check_email, name='cms_check_email'),
    url(r'^email_success/$', views.email_success, name='cms_email_success'),
    # 第三部分：文章管理等
    url(r'^article_manage/(?P<page>\d+)/(?P<category_id>\d+)/$', views.article_manage, name='cms_article_manage'),
    url(r'^add_article/$', views.add_article, name='cms_add_article'),
    url(r'^edit_article/(?P<pk>[\w\-]+)$', views.edit_article, name='cms_edit_article'),
    url(r'^delete_article/$', views.delete_article, name='cms_delete_article'),
    url(r'^top_article/$', views.top_article, name='cms_top_article'),
    url(r'^untop_article/$', views.untop_article, name='cms_untop_article'),
    url(r'^add_tag/$', views.add_tag, name='cms_add_tag'),
    # 第四部分：分类管理等
    url(r'^category_manage/$', views.category_manage, name='cms_category_manage'),
    url(r'^add_category/$', views.add_category, name='cms_add_category'),
    url(r'^edit_category/$', views.edit_category, name='cms_edit_category'),
    url(r'^delete_category/$', views.delete_category, name='cms_delete_category'),
    # 测试：用来批量添加文章
    url(r'^test/$', views.test)
]