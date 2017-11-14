# coding=utf-8
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
django.setup()
from django.contrib.auth.models import User
import article.models

user = User.objects.filter(username="xiaoweizbc").first()

# 删分类
article.models.CategoryModel.objects.all().delete()
# 增分类
a1 = article.models.CategoryModel(name="基础")
a2 = article.models.CategoryModel(name="高级")
a3 = article.models.CategoryModel(name="框架")
a1.save()
a2.save()
a3.save()
# 查分类
cate = article.models.CategoryModel.objects.filter(name="基础").first()

# 删标签
article.models.TagModel.objects.all().delete()
# 增标签
a1 = article.models.TagModel(name="python")
a2 = article.models.TagModel(name="java")
a3 = article.models.TagModel(name="php")
a1.save()
a2.save()
a3.save()
# 查标签
tag = article.models.TagModel.objects.filter(name__contains="pytho")

# 删文章
article.models.ArticleModel.objects.all().delete()
# 增文章
i = 1
while i <= 10:
    a = article.models.ArticleModel(author=user, title="标题"+str(i), category=cate, desc="描述"+str(i), content_html="内容"+str(i), tags=tag)
    a.save()
    i += 1
# 查文章
x = article.models.ArticleModel.objects.filter(title__contains="标题1")
