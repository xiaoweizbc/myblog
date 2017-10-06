# -*- coding: utf-8 -*-
from cmsauth.models import CmsUser


def CmsContextProcessor(request):
    user = request.user
    # 给user添加一个avatar属性
    # avatar属性存储在CmsUser里面
    # 相当于把CmsUser的avatar属性添加到user当中

    # 如果user没有avatar属性,就需要添加\
    if not hasattr(user, 'avatar'):
        cmsuser = CmsUser.objects.filter(user__pk=user.pk).first()
        if cmsuser:
            setattr(user, 'avatar', cmsuser.avatar)

    return {'user': user}
