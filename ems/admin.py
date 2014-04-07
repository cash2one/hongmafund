#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# Author: cbin
# mail: yu.cbin@gmail.com
from django.contrib import admin
#import xadmin
from ems.models import *

class NewsCategoryAdmin(object):
    fields = ('title','keywords','description',)
    #readonly_fields = ("registerdate",)
    list_filter = ('title',)
    list_display = ('title','keywords','description',)
    list_per_page = 10

class ArticleAdmin(object):
    fields = ('title','keywords','summary','className','source','writer','article_time','content',)
    readonly_fields = ("articletime",)
    list_filter = ('title','keywords','className','source','writer',)
    list_display = ('title','keywords','summary','className','source','writer','article_time',)
    list_per_page = 10

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

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserProfileAdmin(UserAdmin):
    inlines=(UserProfileInline, )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)

xadmin.site.register(NewsCategory, NewsCategoryAdmin)
xadmin.site.register(Article, ArticleAdmin)
#xadmin.site.register(ProductCategory, ProductCategoryAdmin)
#xadmin.site.register(ProductArticle, ProductArticleAdmin)