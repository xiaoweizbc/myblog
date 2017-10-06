# coding=utf-8
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
django.setup()

from article.models import TagModel, ArticleModel, CategoryModel
from django.contrib.auth.models import User

user = User.objects.filter(username="dongshan").first()
cate = CategoryModel.objects.filter(name="人文").first()
tag = TagModel.objects.filter(name__contains="吃货")

i = 1
while i < 100:
    a = ArticleModel(author=user, title="腰吃就吃大腰子 0" + str(i), category=cate, desc="腰子", content_html="我爱大腰子", tags=tag)
    a.save()
    i += 1
