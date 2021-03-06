# -*- coding: utf-8 -*-
from django import forms
from utils.captcha.mycaptcha import Captcha
import json
from utils import myjson
from api.common.forms import BaseForm


# 第一部分
class LoginForm(BaseForm):
    username = forms.CharField(max_length=10, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)
    captcha = forms.CharField(max_length=4, min_length=4)
    remember = forms.BooleanField(required=False)  # required=False指非必须：用户有可能不需要“记住我”,那么这个参数有可能就没有

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha', None)
        print "captcha =",captcha
        if not Captcha.check_captcha(captcha):
            pass  # 此语句作用是不校验验证码直接通过，方便测试
            # raise forms.ValidationError(u'验证码错误!')
        return captcha


# 第二部分
class UpdateProfileForm(BaseForm):
    avatar = forms.URLField(max_length=100, required=False)  # required=False指非必须
    username = forms.CharField(max_length=10, min_length=4, required=False)  # required=False指非必须


class UpdateEmailForm(BaseForm):
    email = forms.EmailField(required=True)  # required=True指必须


class AddCategoryForm(BaseForm):
    categoryname = forms.CharField(max_length=20)


class AddTagForm(BaseForm):
    tagname = forms.CharField(max_length=20)


class AddArticleForm(BaseForm):
    title = forms.CharField(max_length=200)
    category = forms.IntegerField(required=True)
    desc = forms.CharField(max_length=200, required=False)
    thumbnail = forms.URLField(max_length=100, required=False)
    content_html = forms.CharField()

# author,tags
# tags是通过数组的形式进行上传的,forms没有合适的
# field来进行验证,所以不放在form中进行验证

# author也不需要,因为当前登录的页面就是author


class UpdateArticleForm(AddArticleForm):
    uid = forms.UUIDField()


class DeleteArticleForm(BaseForm):
    uid = forms.UUIDField(error_messages={'required': u'文章id不能少'})


class TopArticleForm(DeleteArticleForm):
    pass


class CategoryForm(BaseForm):
    category_id = forms.IntegerField()


class EditCategoryForm(CategoryForm):
    name = forms.CharField()
