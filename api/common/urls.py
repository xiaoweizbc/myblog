# -*- coding: utf-8 -*-
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^captcha/', views.captcha, name='common_captcha'),
]
