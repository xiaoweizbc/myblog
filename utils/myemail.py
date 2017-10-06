# -*- coding: utf-8 -*-
import hashlib
from django.core.cache import cache
from django.shortcuts import reverse
from django.conf import settings
import time
from django.core import mail


def send_email(request, email, check_url, cache_data=None, subject=None, message=None):  # email和check_url是必选参数
    code = hashlib.md5(str(time.time()) + email).hexdigest()
    if cache_data:
        cache.set(code, cache_data, 120)
    else:  # 邮箱验证走这条
        cache.set(code, email, 120)
    url = request.scheme + '://' + request.get_host() + reverse(check_url, kwargs={'code': code})
    if not subject:  # 邮箱验证走这条
        subject = u'邮箱验证'
    if not message:  # 邮箱验证走这条
        #  message中应该包含验证的链接
        message = u'博客验证链接,点击 ' + url + u'  ,请在10分钟内完成注册。工作人员不会向您索取验证码，请勿泄露。消息来自：xx的博客'
    from_mail = settings.EMAIL_HOST_USER  # 宿主邮箱
    recipient_list = [email]  # 目标邮箱列表
    if mail.send_mail(subject, message, from_mail, recipient_list):
        print "发送成功"
        return True
    else:
        print "发送失败"
        return False
