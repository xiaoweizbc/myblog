# coding=utf-8
from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('api.front.urls')),  # 前台：http://127.0.0.1:8000/
    url(r'^cms/', include('api.cms.urls')),  # 后台：http://127.0.0.1:8000/cms/
    url(r'^comm/', include('api.common.urls')),  # 公共组件
    url(r'^auth/', include('frontauth.urls')),  # 测试用：http://127.0.0.1:8000/auth/
]
