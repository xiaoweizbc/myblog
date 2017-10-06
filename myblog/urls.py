# coding=utf-8
from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('api.front.urls')),  # 前台
    url(r'^cms/', include('api.cms.urls')),  # 后台
    url(r'^comm/', include('api.common.urls')),  #
    url(r'^auth/', include('frontauth.urls')),  #
]
