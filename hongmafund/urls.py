# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView
#from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required as auth

import xadmin
xadmin.autodiscover()

#from .views import index
#from djadmin_export import register
#register.auto_register_exporters()

from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT },name='media'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT },name='static'),
    url(r'^$', 'ems.views.index',name='index'),
    #(r'^accounts/', include('profiles.urls')),
    # url(r'^hongmafund/', include('hongmafund.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    #内容页
    url(r'^spzh/simu?(\d+)88\.html$', 'ems.views.article_content', name='dlsp'),
    url(r'^spzh/simu?(\d+)88\.html$', 'ems.views.article_content', name='dlqh'),
    url(r'^spzh/simu?(\d+)88\.html$', 'ems.views.article_content', name='qqqp'),
    url(r'^spzh/simu?(\d+)88\.html$', 'ems.views.article_content', name='qqqh'),
    url(r'^dyzh/simu?(\d+)88\.html$', 'ems.views.article_content', name='yyys'),
    url(r'^dyzh/simu?(\d+)88\.html$', 'ems.views.article_content', name='yyyx'),
    url(r'^smjj/simu?(\d+)88\.html$', 'ems.views.article_content', name='dlsmjj'),
    url(r'^smjj/simu?(\d+)88\.html$', 'ems.views.article_content', name='qqsmjj'),
    url(r'^zzvip/simu?(\d+)88\.html$', 'ems.views.article_content', name='srcp'),
    url(r'^zzvip/simu?(\d+)88\.html$', 'ems.views.article_content', name='zzvip2'),
    #导航大分类
    #url(r'^([A-Za-z]+)\.html$', 'ems.views.article_gory', name='cate'),

    url(r'^spzh\.html$', 'ems.views.spzh_list', name='spzh'),
    url(r'^dyzh\.html$', 'ems.views.ddzh_list', name='dyzh'),
    url(r'^smjj\.html$', 'ems.views.smjj_list', name='smjj'),
    url(r'^zzvip\.html$', 'ems.views.zzvip_list', name='zzvip'),

    url(r'^company\.html$', 'ems.views.company', name='company'),
    url(r'^contacts\.html$', 'ems.views.contacts', name='contacts'),
    url(r'^services\.html$', 'ems.views.services', name='service'),
    url(r'^about\.html$', 'ems.views.about', name='about'),

    url(r'^chart/([A-Za-z]+)\.html$', 'hmchart.views.linewithfocuschart', name='chart'),

    url(r'^gsmap\.html$', 'ems.views.gsmap', name='gsmap'),
    url(r'^ggfw\.html$', 'ems.views.ggfw', name='ggfw'),
    url(r'^products\.html$', 'ems.views.products', name='products'),
    url(r'^hzhb\.html$', 'ems.views.hzhb', name='hzhb'),
    url(r'^flsm\.html$', 'ems.views.flsm', name='flsm'),
    url(r'^job\.html$', 'ems.views.job', name='job'),

    #二级栏目
    #spzh/dlsp.html'>大陆A股
    #spzh/dlqh.html'>大陆期货
    #spzh/qqgp.html'>全球股票
    #spzh/qqqh.html'>全球期货
    url(r'^spzh/([A-Za-z]+)\.html$', 'ems.views.article_category', name='spzh'),
    #dyzh/yyys.html'>私人操盘
    #dyzh/yyyx.html'>至尊vip
    url(r'^dyzh/([A-Za-z]+)\.html$', 'ems.views.article_category', name='dyzh'),
    #smjj/dlsmjj.html'>大陆A股
    #smjj/qqsmjj.html'>大陆期货
    url(r'^smjj/([A-Za-z]+)\.html$', 'ems.views.article_category', name='smjj'),
    #zzvip/srcp.html'>私人操盘
    #zzvip/zzvip.html'>至尊vip
    url(r'^zzvip/([A-Za-z]+)\.html$', 'ems.views.article_category', name='zzvip'),
    #apps urls
    url(r'^accounts/', include('registration.urls')),
    url(r'^user/', include('ems.urls')),
    url(r'^charts/', include('hmchart.urls')),
    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
#urlpatterns = patterns('',url(r'xadmin/', include(xadmin.site.urls)),)