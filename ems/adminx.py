#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# Author: cbin
# mail: yu.cbin@gmail.com
#from django.contrib import admin

from ems.models import NewsCategory,Article,UserProfile#,Employee#ProductCategory,ProductArticle
from rte.widgets import Ueditor
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

from django.contrib import admin
import xadmin
#from django.contrib.auth.admin import UserAdmin
from xadmin.plugins.auth import UserAdmin
from xadmin.plugins.inline import InlineModelAdmin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#from xadmin.plugins.auth import get_user_model
"""
class UserProfileInline(InlineModelAdmin):
    model = UserProfile
    can_delete = False

class UserProfileAdmin(UserAdmin):
    inlines=(UserProfileInline, )

xadmin.site.unregister(get_user_model())
xadmin.site.register(get_user_model(), UserProfileAdmin)
"""
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
"""
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    #verbose_name_plural = 'employee'
# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (EmployeeInline,)

# Re-register UserAdmin#
#xadmin.site.unregister(User)
#xadmin.site.register(User, UserAdmin)
"""
class UserProfileAdmin2(object):
    fields = ('user','mobile','qq','address','user_type','phone','login_ip','logins',)
    #readonly_fields = ("user_type",)
    list_filter = ('mobile','qq',)
    list_display_links = ('id',)
    list_display = ('id','user','mobile','qq','user_type','login_ip','logins',)
    list_per_page = 10
xadmin.site.register(UserProfile,UserProfileAdmin2)

class NewsCategoryAdmin(object):
    fields = ('id','title','slug','keywords','description',)
    #readonly_fields = ("registerdate",)
    list_filter = ('title',)
    list_display_links = ('id',)
    list_display = ('id','title','slug','keywords','description',)
    list_per_page = 10
    #

class ArticleAdmin(object):
    fields = ('title','keywords','summary','className','source','writer','article_time','content','added_by')
    #readonly_fields = ("article_time",)
    style_fields = {"content": 'ueditor'}
    list_filter = ('title','keywords','className','source','writer',)
    list_display = ('id','className','title','article_time','added_by')
    list_per_page = 10
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'upload'))
    #此处代码是指定上传文件的路径，目录权限要设置为777，windows上要设置为everyone 读写
    def get_field_style(self, db_field, style, **kwargs):
        if style in ('ueditor',):
            attrs = {'widget': Ueditor}  # 此处是顶部的widget引用
            return attrs
    def save_model(self, obj,request,**kwagrs):
        if getattr(obj, 'added_by', None) is None:
            obj.added_by = request.user
        obj.last_modified_by = request.user
        obj.save()
"""    def queryset(self, request):
        qs = super(ArticleAdmin, self).queryset(request)
        # If super-user, show all comments
        if request.user is None:
            request.user = 'root'
        if request.user.is_superuser:
            return qs
        return qs.filter(added_by=request.user)"""
"""
class ProductCategoryAdmin(object):
    fields = ('className','title','keywords','description',)
    #readonly_fields = ("registerdate",)
    list_filter = ('className',)
    list_display = ('className','title','keywords','description',)
    list_per_page = 10

class ProductArticleAdmin(object):
    fields = ('title','keywords','summary','className','productImg','thumbnail','source','writer','productime','content',)
    readonly_fields = ('thumbnail',"productime",)
    list_filter = ('title','className','productime',)
    list_display = ('admin_thumbnail','title','className','productime',)
    list_per_page = 10
"""

xadmin.site.register(NewsCategory, NewsCategoryAdmin)
xadmin.site.register(Article, ArticleAdmin)
#xadmin.site.register(ProductCategory, ProductCategoryAdmin)
#xadmin.site.register(ProductArticle, ProductArticleAdmin)