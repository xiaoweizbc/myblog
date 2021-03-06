# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from forms import LoginForm, UpdateProfileForm, UpdateEmailForm, AddCategoryForm, AddTagForm, AddArticleForm, \
    UpdateArticleForm, DeleteArticleForm, TopArticleForm, CategoryForm, EditCategoryForm
from django.shortcuts import render, redirect, reverse
from django.core.cache import cache
from cmsauth.models import CmsUser
from qiniu import Auth, put_file
import qiniu.config
from django.views.decorators.http import require_http_methods
from django.core import mail
import hashlib
import time
from article.models import ArticleModel, CategoryModel, TagModel, TopModel
from utils import myjson
from django.conf import settings
from django.forms import model_to_dict
from django.db.models import Count
from utils.myemail import send_email


# 第一部分：cms_login.html
# 渲染cms_login.html
def cms_login(request):  # 登录函数
    if request.method == 'GET':
        print "request.GET过来的数据 =", request.GET
        return render(request, 'cms_login.html')
    else:
        print "request.POST过来的数据 =", request.POST
        print "request.POST.get()"  # 用这种方法，及时没有remember这个参数，也不会报错，会默认为None
        print "request.POST过来的数据username =", request.POST.get("username")
        print "request.POST过来的数据password =", request.POST.get("password")
        print "request.POST过来的数据captcha =", request.POST.get("captcha")
        print "request.POST过来的数据remember =", request.POST.get("remember")
        print "request.POST[]"  # 不要用这种方法，因为request.POST[]可能没有remember这个参数
        # print "request.POST过来的数据username =", request.POST["username"]
        # print "request.POST过来的数据password =", request.POST["password"]
        # print "request.POST过来的数据captcha =", request.POST["captcha"]
        # print "request.POST过来的数据remember =", request.POST["remember"]
        form = LoginForm(request.POST)
        if form.is_valid():  # form.is_valid()表示表单设置的条件均成立
            username = form.cleaned_data.get('username', None)
            password = form.cleaned_data.get('password', None)
            captcha = form.cleaned_data.get('captcha', None)
            remember = form.cleaned_data.get('remember', None)
            print "form的数据username =", username
            print "form的数据password =", password
            print "form的数据captcha =", captcha
            print "form的数据remember =", remember
            # 1. 先用authenticate进行验证
            user = authenticate(username=username, password=password)
            print "user =", user
            print "type(user) =", type(user)
            if user:
                # 2. 需要登录,
                # 3. 我们的login视图函数不要和login重名
                login(request, user)
                # 判断如果有remember,那么说明需要记住,使用None将
                # 使用settings.py中SESSION_COOKIE_AGE指定的值,
                # 这个值默认是14天
                if remember:  # 如果勾选了“记住我”
                    print "用户勾选了“记住我”"
                    request.session.set_expiry(None)
                    """
                 一、request.session.set_expiry(value)；可以传递四种不同的值给它：
                    *如果value是个整数，session会在些秒数后失效。
                    *如果value是个datatime或timedelta，session就会在这个时间后失效。
                    *如果value是0, 用户关闭浏览器session就会失效。 // 我们用的就是这种方式
                    *如果value是None, session会依赖全局session失效策略。
                 """
                else:  # 如果没有勾选“记住我”
                    print "用户没有勾选“记住我”"
                    request.session.set_expiry(0)  # 浏览器一旦关闭,session就会过期

                nexturl = request.GET.get('next')
                print "nexturl =", nexturl
                if nexturl:  # 如果nexturl非空，则跳转到原来的地址
                    return redirect(nexturl)
                else:  # 如果为空，则默认跳转到主页，查路由表得知，即article_manage
                    return redirect(reverse('cms_index'))
            else:
                return render(request, 'cms_login.html', {'error': '用户名或密码错误!'})
        else:
            return render(request, 'cms_login.html', {'error': form.get_error()})


def cms_logout(request):  # 登出函数
    logout(request)
    return redirect(reverse('cms_login'))


# 第二部分：cms_settings.html，cms_email.html，cms_emailsuccess.html
# 渲染cms_settings.html
@login_required
def cms_settings(request):  # 个人设置函数
    # 1. 可以修改用户名
    # 2. 可以修改头像
    # 3. 可以修改邮箱
    return render(request, 'cms_settings.html')


@login_required
@require_http_methods(['POST'])
def update_profile(request):  # 更新简介函数
    """
    1. 更新用户名(username)
    2. 更新头像(avatar)
    """
    print "request.POST过来的数据 =", request.POST
    print "request.POST过来的数据username =", request.POST.get("username")
    print "request.POST过来的数据avater =", request.POST.get("avatar")  # 如果没有就是空值
    form = UpdateProfileForm(request.POST)
    if form.is_valid():
        avatar = form.cleaned_data.get('avatar', None)
        username = form.cleaned_data.get('username', None)
        print "form中的数据username =", username
        print "form中的数据avater =", avatar
        # 1.更新用户名
        user = User.objects.get(username=username)
        print "修改的User =", user
        user.username = username
        user.save()
        # 2.更新头像
        cmsuser = CmsUser.objects.filter(user__pk=user.pk).first()
        if not cmsuser:  # 如果CmsUser这个表里没有数据和user一一对应（没有上传过头像），就应该新建，然后将avater保存进去
            cmsuser = CmsUser(avatar=avatar, user=user)
        else:  # 如果CmsUser这个表里已经有数据和user一一对应（已经上传过头像），就直接更新avater
            if avatar != "":
                cmsuser.avatar = avatar
            else:
                pass
        cmsuser.save()
        return myjson.json_result()
    else:
        return form.get_error_response()


@require_http_methods(['GET'])
def get_token(request):  # 七牛token函数
    """
    1. 客户端在上传图片到七牛之前,需要先从业务服务器
    上获取token,本函数就是获取token的函数
    2. 客户端获取到token后,拿到token后把token和图片一起上传到七牛服务器
    3. 七牛收到token和图片后,会判断当前token是否有效,如果有效,则会返回图片名到客户端和业务服务器.
    """
    # 1. 先要设置AccessKey和SecretKey
    access_key = "EoQLmj6KZb1a5Z6fpnqnoVmWUls-ze_d-v0Dyjtb"
    secret_key = "u4vRYzSjdk3UF7rTRY3quEkBQnYUaC00hne29vmh"
    # 2. 授权
    q = Auth(access_key, secret_key)
    # 3. 设置七牛空间
    bucket_name = 'test'
    # 4. 生成token
    token = q.upload_token(bucket_name)
    # 5. 返回token,key必须为uptoken
    # return JsonResponse({'uptoken':token})
    # return myjson.json_result(data={'uptoken':token})
    return myjson.json_result(kwargs={'uptoken': token})


# 渲染cms_email.html
@login_required
@require_http_methods(['GET', 'POST'])
def update_email(request):  # 更新email函数
    if request.method == 'GET':
        return render(request, 'cms_email.html')
    else:
        print "request.POST过来的数据 =", request.POST
        print "request.POST过来的数据email =", request.POST.get("email")
        form = UpdateEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email', None)
            print "form中的数据email =", email
            if send_email(request, email, 'cms_check_email'):  # 肯定都是发送成功的啦~
                return redirect(reverse('cms_email_success'))
            else:
                return redirect(reverse('cms_email_fail'))
        else:
            return render(request, 'cms_email.html', {'error': form.errors})


# 渲染cms_emailsuccess.html
@login_required
@require_http_methods(['GET'])
def email_success(request):
    return render(request, 'cms_emailsuccess.html')


@require_http_methods(['GET'])
def check_email(request, code):
    """
    验证邮箱的url
    """
    if len(code) > 0:  # 需要知道用户之前修改邮箱的时候填的是什么邮箱
        # 通过code,在缓存里获取email
        email = cache.get(code)
        print email
        if email:
            user = request.user
            user.email = email
            # update_fileds这个参数可以指定需要保存哪些字段
            # 好处在于不需要保存没有更新的字段,提升效率
            user.save(update_fields=['email'])
            return HttpResponse(u'邮箱修改成功')
        else:
            return HttpResponse(u'该链接已经失效')
    else:
        return HttpResponse(u'该链接已经失效')


# 第三部分：cms_article_manage.html，cms_add_article.html，cms_edit_article.html
# 渲染cms_article_manage.html
@login_required
def article_manage(request, page=1, category_id=0):  # 文章相关操作
    # pages c_page t_page
    # 获取所有的文章
    categoryId = int(category_id)
    currentPage = int(page)
    numPage = int(settings.NUM_PAGE)
    articles = None
    if categoryId > 0:
        articles = ArticleModel.objects.all().filter(category__pk=categoryId).order_by('-top__create_time',
                                                                                       '-release_time')
    else:
        articles = ArticleModel.objects.all().order_by('-top__create_time', '-release_time')
    start = (currentPage - 1) * numPage
    end = start + numPage
    # 一页加载的文章数
    # 先算出文章的总数
    articleCount = articles.count()
    # 对文章进行切片
    articles = articles[start:end]
    # 总共有多少页
    pageCount = articleCount / numPage
    if articleCount % numPage > 0:
        pageCount += 1

    # pages
    # < [1] 2 3 4 5 >
    # < 6 [7] 8 9 10 >
    # < [11] 12 13 14 15 >
    # 用来装当前页面的所有分页序号
    pages = []

    # 先往前面找
    tmpPage = currentPage - 1
    # 满足最大的条件,tmpPage不能小于1
    while tmpPage >= 1:
        if tmpPage % 5 == 0:
            break
        else:
            pages.append(tmpPage)
            tmpPage -= 1

    # 往后面找
    tmpPage = currentPage
    while tmpPage <= pageCount:
        if tmpPage % 5 == 0:
            pages.append(tmpPage)
            break
        else:
            pages.append(tmpPage)
            tmpPage += 1

    pages.sort()

    # 获取所有的分类
    categorys = CategoryModel.objects.all()

    context = {
        'c_page': currentPage,
        't_page': pageCount,
        'pages': pages,
        'articles': articles,
        'categorys': categorys,
        'c_category': categoryId,
    }
    return render(request, 'cms_article_manage.html', context=context)


# 渲染cms_add_article.html
@login_required
def add_article(request):
    if request.method == 'GET':
        categorys = CategoryModel.objects.all()
        tags = TagModel.objects.all()
        data = {
            'categorys': categorys,
            'tags': tags
        }
        return render(request, 'cms_add_article.html', data)
    else:
        form = AddArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content_html = form.cleaned_data.get('content_html')
            tags = request.POST.getlist('tags[]')
            user = request.user

            categoryModel = CategoryModel.objects.filter(pk=category).first()

            articleModel = ArticleModel(title=title, desc=desc, thumbnail=thumbnail, content_html=content_html,
                                        author=user, category=categoryModel)
            articleModel.save()
            # 添加tags的多对多

            if tags:
                for tag in tags:
                    tagModel = TagModel.objects.filter(pk=int(tag)).first()
                    if tagModel:
                        articleModel.tags.add(tagModel)

            return myjson.json_result(data={})

        else:
            return form.get_error_response()


# 渲染cms_edit_article.html
@login_required
@require_http_methods(['GET', 'POST'])
def edit_article(request, pk=''):
    if request.method == 'GET':
        article = ArticleModel.objects.filter(pk=pk).first()
        articleDict = model_to_dict(article)
        articleDict['tags'] = []
        for tagModel in article.tags.all():
            articleDict['tags'].append(tagModel.id)
        context = {
            'article': articleDict,
            'categorys': CategoryModel.objects.all(),
            'tags': TagModel.objects.all()
        }
        return render(request, 'cms_edit_article.html', context)
    else:
        form = UpdateArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content_html = form.cleaned_data.get('content_html')
            tags = request.POST.getlist('tags')
            uid = form.cleaned_data.get('uid')
            articleModel = ArticleModel.objects.filter(pk=uid).first()
            if articleModel:
                articleModel.title = title
                articleModel.desc = desc
                articleModel.thumbnail = thumbnail
                articleModel.content_html = content_html
                articleModel.category = CategoryModel.objects.filter(pk=category).first()
                articleModel.save()

                if tags:
                    for tag in tags:
                        tagModel = TagModel.objects.filter(pk=tag).first()
                        articleModel.tags.add(tagModel)

            return myjson.json_result()
        else:
            return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def delete_article(request):
    form = DeleteArticleForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        articleModel = ArticleModel.objects.filter(pk=uid).first()
        if articleModel:
            articleModel.delete()
            return myjson.json_result()
        else:
            return myjson.json_params_error(message=u'该博客不存在')
    else:
        return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def top_article(request):
    # method(GET,POST)
    # 参数
    # wiki
    form = TopArticleForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        articleModel = ArticleModel.objects.filter(pk=uid).first()

        if articleModel:
            if not articleModel.thumbnail:
                return myjson.json_params_error(message=u'有缩略图的文章才能置顶')
            topModel = articleModel.top
            if not topModel:
                topModel = TopModel()

            # 如果存在,也save一下,这样就会更新operate_time了
            topModel.save()

            articleModel.top = topModel
            articleModel.save(update_fields=['top'])
            return myjson.json_result()
        else:
            return myjson.json_params_error(message=u'该文章不存在')
    else:
        return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def untop_article(request):
    form = TopArticleForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        articleModel = ArticleModel.objects.filter(pk=uid).first()
        if articleModel:
            if articleModel.top:
                topModel = articleModel.top
                topModel.delete()
                return myjson.json_result()
            else:
                return myjson.json_params_error(message=u'本文章还未置顶呢')
        else:
            return myjson.json_params_error(message=u'该文章不存在')
    else:
        return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def add_tag(request):
    form = AddTagForm(request.POST)
    if form.is_valid():
        tagname = form.cleaned_data.get('tagname')
        # 先判断一下数据库中是否已经存在同名的标签
        resultTag = TagModel.objects.filter(name=tagname).first()
        if not resultTag:
            # 如果没有,说明可以添加
            tagModel = TagModel(name=tagname)
            tagModel.save()
            return myjson.json_result(data={'id': tagModel.id, 'name': tagModel.name})
        else:
            return myjson.json_params_error(message=u'不能设置同名标签!')
    else:
        return form.get_error_response()


# 第四部分
# 渲染cms_category_manage.html
@login_required
@require_http_methods(['GET'])
def category_manage(request):
    if request.method == 'GET':
        # annotate这个函数会给QuerySet当中的所有模型添加属性,具体的属性根据提供的聚合函数而定
        categorys = CategoryModel.objects.all().annotate(num_articles=Count('articlemodel')).order_by('-num_articles')
        context = {
            'categorys': categorys
        }
        return render(request, 'cms_category_manage.html', context)


@login_required
@require_http_methods(['POST'])
def edit_category(request):
    form = EditCategoryForm(request.POST)
    if form.is_valid():
        categoryId = form.cleaned_data.get('category_id')
        name = form.cleaned_data.get('name')
        categoryModel = CategoryModel.objects.filter(pk=categoryId).first()
        if categoryModel:
            categoryModel.name = name
            categoryModel.save(update_fields=['name'])
            return myjson.json_result()
        else:
            return myjson.json_params_error(message=u'该分类不存在')
    else:
        return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def delete_category(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        categoryId = form.cleaned_data.get('category_id')
        categoryModel = CategoryModel.objects.filter(pk=categoryId).first()
        if categoryModel:
            # 首先拿到该分类下的文章数量
            articleCount = categoryModel.articlemodel_set.all().count()
            # 如果文章数量大于0,就不让删除
            if articleCount > 0:
                return myjson.json_params_error(message=u'该分类下还存在文章,不能删除!')
            else:
                categoryModel.delete()
                return myjson.json_result()
        else:
            return myjson.json_params_error(message=u'该分类不存在')
    else:
        return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def add_category(request):
    form = AddCategoryForm(request.POST)
    if form.is_valid():
        categoryname = form.cleaned_data.get('categoryname', None)
        resultCategory = CategoryModel.objects.filter(name=categoryname).first()
        if not resultCategory:
            categoryModel = CategoryModel(name=categoryname)
            categoryModel.save()
            return myjson.json_result(data={'id': categoryModel.id, 'name': categoryModel.name})
        else:
            # return JsonResponse({'error':u'不能設置同名的分類!','code':403})
            return myjson.json_params_error(message=u'不能設置同名的分類!')
    else:
        # return JsonResponse({'error':form.errors.as_json,'code':'403'});
        return myjson.json_params_error(message=u'表单验证失败')


# 第五部分
def test(request):
    for x in xrange(0, 100):
        title = u'博客标题%s' % x
        category = CategoryModel.objects.all().first()
        content_html = u'博客内容%s' % x
        articleModel = ArticleModel(title=title, content_html=content_html, category=category)
        articleModel.save()
    return myjson.json_result()
