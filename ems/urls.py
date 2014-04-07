# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView
#from django.contrib import admin
from ems.views import UserProfileDetailView,UserProfileEditView,UserIndexView
from django.contrib.auth.decorators import login_required as auth

urlpatterns = patterns('',
	url(r'^$', UserIndexView, name='user'),
	#url(r'^profile/$', UserProfileDetailView.as_view(), name="profiles"),
	url(r'^edit_profile/$', auth(UserProfileEditView.as_view()), name="edit_profile"),
	#url(r'^linechart/$', demo_linechart, name='demo_linechart'),
    #url(r'^linechart_without_date/$', demo_linechart_without_date, name='demo_linechart_without_date'),
	#url(r'^linewithfocuschart/$', demo_linewithfocuschart, name='demo_linewithfocuschart'),
    url(r'^(?P<slug>\w+)/$', UserProfileDetailView.as_view(), name="profile"),
    #(r'^accounts/', include('profiles.urls')),
)
