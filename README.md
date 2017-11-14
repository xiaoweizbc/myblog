# 项目说明
###project structure（从项目根目录出发）：
0.创建项目时原始目录和文件（不作说明）
	manage.py
	myblog
		__init__.py
		settings.py
		urls.py
		wsgi.py
1.api应用（也可以理解成模块&包）设计了三个子应用（注意python模块必须要有__init__.py文件支撑，否则django系统无法识别）
	cms目录：有关后台内容管理系统，其中包括
		文件__init__.py 
		目录static（存放静态文件）
		目录templates（存放模板文件）
		文件form.py（Django表单：对用户提交的表单数据进行处理）
		文件url.py（二级路由）
		文件views.py（视图）
	common目录：可供各个app一起共用的api，我们选择新建一个模块包来管理公用
		文件__init__.py 
		目录static（各个app共用的静态文件）
		目录templates（各个app共用的模板文件）
		文件form.py（各个app共用的Django表单）
		文件url.py（各个app共用的路由）
		文件views.py（各个app共用的视图）
	front目录：有关前台博客系统，其中包括
		文件__init__.py 
		目录static（存放静态文件）
		目录templates（存放模板文件）
		文件form.py（Django表单：对用户提交的表单数据进行处理）
		文件url.py（二级路由）
		文件views.py（视图）
2.article应用用于生成文章相关数据模型
	文件__init__.py 
	文件models.py
3.cmsauth应用用于生成后台内容管理系统用户相关数据模型
	文件__init__.py 
	文件models.py
4.contextprocessor应用用于定义后台内容管理系统的上下文处理器
	文件__init__.py 
	文件cms_contextprocessor.py
###project details
a.cms模板继承关系
	comm_bootstrap.html(最底层的父模板，下面的都是继承它的)
		cms_login.html
		cms_base.html（网页上方导航栏nav标签）
			cms_base_manage.html
				cms_article_manage.html
				cms_category_manage.html
			cms_base_article.html
				cms_add_article.html
				cms_edit_article.html
			cms_settings.html
			cms_email.html
			cms_email_success.html
	cms_tag_templates.html（暂时没有继承任何父模板）
附：cms注册页面暂时没做，要在Terminal中输入python2 manage.py shell来操作：
b.front模板继承关系
	comm_bootstrap.html(最底层的父模板，下面的都是继承它的)
		front_sign_base.html
		front_base.html（网页上方导航栏nav标签）
			front_article_detail.html
			front_article_list.html(include front_artclelist_tpl.html)
        front_forgetpwd.html
        front_resetpwd.html
        front_sign_base.html
            front_signin.html
            front_signup.html
 `
from django.contrib.auth.models import User  
user = User.objects.create_user(username='***', email=None, password=None')  # 创建用户
user.last_name = 'last_name'  # 修改用户信息
user.save()
u = User.objects.get(username='username')
u.set_password(raw_password='new password')  # 修改密码
u.save()
```
已创建cms（数据表auth_user）
	用户名：xiaoweizbc   密码：111111
	用户名：hiumy   密码：111111
已创建front（数据表frontauth_frontusermodel）
	邮箱：xiaoweizbc@163.com   密码：123456
	邮箱：358083856@qq.com   密码：123456



