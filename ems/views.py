# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpRequest
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404,RequestContext
from django.contrib.sites.models import Site, RequestSite, get_current_site
from ems.models import *
from django.http import HttpResponseRedirect
from ems.models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model

from django.views.generic.edit import UpdateView
from ems.models import UserProfile
from ems.forms import UserProfileForm
from django.core.urlresolvers import reverse

from hmchart.views import index_chart
from django.shortcuts import render_to_response
import random
import datetime
import time

GLOBLE_GORY ={
    'about':'',
    'spzh':'',
    'dyzh':'',
    'smjj':'',
    'zzvip':'',
    'cpcd':'',
    'service':'',
    }
#二级栏目
#spzh/dlsp.html'>大陆A股
#spzh/dlqq.html'>大陆期货
#spzh/qqgp.html'>全球股票
#spzh/qqqh.html'>全球期货
#dyzh/yyys.html'>私人操盘
#dyzj/yyyx.html'>至尊vip
#smjj/dlsmjj.html'>大陆A股
#smjj/qqsmjj.html'>大陆期货
#zzvip/srcp.html'>私人操盘
#zzvip/zzvip.html'>至尊vip
GLOBLE_SECOND ={
    'dlsp':u'中国大陆A股实盘账户',
    'dlqh':u'中国大陆期货实盘账户',
    'qqgp':u'全球股票实盘账户',
    'qqqh':u'全球期货实盘账户',
    'yyys':u'1亿人民币以上实盘账户',
    'yyyx':u'1亿人民币以下实盘账户 ',
    'dlsmjj':u'中国大陆地区私募基金',
    'qqsmjj':u'全球私募基金',
    'srcp':u'雇佣专属私人操盘手',
    'zzvip':u'雇佣专属至尊VIP操盘团队',
    }

GLOBLE_SECOND_URL ={
    'dlsp':'spzh',
    'dlqh':'spzh',
    'qqgp':'spzh',
    'qqqh':'spzh',
    'yyys':'dyzh',
    'yyyx':'dyzh',
    'dlsmjj':'smjj',
    'qqsmjj':'smjj',
    'srcp':'zzvip',
    'zzvip':'zzvip',
    }

GLOBLE_CON ={
    u'中国大陆A股实盘账户':'dlsp',
    u'中国大陆期货实盘账户':'dlqh',
    u'全球股票实盘账户':'qqgp',
    u'全球期货实盘账户':'qqqh',
    u'1亿人民币以上实盘账户':'yyys',
    u'1亿人民币以下实盘账户 ':'yyyx',
    u'中国大陆地区私募基金':'dlsmjj',
    u'全球私募基金':'qqsmjj',
    u'雇佣专属私人操盘手':'srcp',
    u'雇佣专属至尊VIP操盘团队':'zzvip',
    }


def UserIndexView(request):
    if request.user.is_authenticated:
        url = str(request.user)
        #print(url)
        return HttpResponseRedirect('/user/'+url)  
    else:
        return HttpResponseRedirect('http://localhost:8000/')

def glob_article_category2(gory):
    gory_name = GLOBLE_SECOND.get(gory)
    #print(gory_name)
    article_by_gory = Article.objects.filter(className__title=gory_name)
    return article_by_gory

class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "profiles/user_detail.html"

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        #article_dlsp = glob_article_category2('dlsp')
        #print(article_dlsp)
        #article_dlqh = glob_article_category2('dlqh')
        #article_qqgp = glob_article_category2('qqgp')
        #article_qqqh = glob_article_category2('qqqh')
        #article_by_gory = list(article_dlsp)+list(article_qqgp)+list(article_dlqh)+list(article_qqqh)
        #print(article_by_gory)
        return user

class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profiles/edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={'slug': self.request.user})




def article_gory(request):
    aa = request.META.get('PATH_INFO')
    #print(request.path)
    return HttpResponse(aa)

def glob_article_category(request,gory):
    gory_name = GLOBLE_SECOND.get(gory)
    #print(gory_name)
    article_by_gory = Article.objects.filter(className__title=gory_name)
    return article_by_gory

def article_category(request,gory):
    gory_url = GLOBLE_SECOND_URL.get(gory)
    gory_name = GLOBLE_SECOND.get(gory)
    gory_seo = NewsCategory.objects.get(title=gory_name)
    article_by_gory = Article.objects.filter(className__title=gory_name)
    #print('test gory')
    return render_to_response('artical_list.html',locals())
    #return HttpResponse(GLOBLE_SECOND.get(gory))

def article_content(request,id):
    article_by_id = Article.objects.get(id=id)
    gory_second_url = GLOBLE_CON.get(article_by_id.className.title,'')
    gory_url = GLOBLE_SECOND_URL.get(gory_second_url,'')
    #print(gory_url)
    return render_to_response('artical_con.html',locals())

@csrf_protect
def index(request):
    article_dlsp = glob_article_category(request,'dlsp')
    #print(article_dlsp)
    article_dlqh = glob_article_category(request,'dlqh')
    article_qqgp = glob_article_category(request,'qqgp')
    article_qqqh = glob_article_category(request,'qqqh')
    article_yyys = glob_article_category(request,'yyys')
    article_yyyx = glob_article_category(request,'yyyx')
    article_dlsmjj = glob_article_category(request,'dlsmjj')
    article_qqsmjj = glob_article_category(request,'qqsmjj')
    article_srcp = glob_article_category(request,'srcp')
    article_zzvip = glob_article_category(request,'zzvip')
    chart,chart2 = index_chart(request)
    #print(chart)
    from hmchart.views import admanager
    ad1,ad2 = admanager(request)
    return render_to_response('index2.html',locals())

def spzh_list(request):
    article_dlsp = glob_article_category(request,'dlsp')
    #print(article_dlsp)
    article_dlqh = glob_article_category(request,'dlqh')
    article_qqgp = glob_article_category(request,'qqgp')
    article_qqqh = glob_article_category(request,'qqqh')
    article_by_gory = list(article_dlsp)+list(article_qqgp)+list(article_dlqh)+list(article_qqqh)
    return render_to_response('artical_list_spzh.html',locals())

def ddzh_list(request):
    article_yyys = glob_article_category(request,'yyys')
    article_yyyx = glob_article_category(request,'yyyx')
    article_by_gory = list(article_yyys)+list(article_yyyx)
    return render_to_response('artical_list_ddzh.html',locals())

def smjj_list(request):
    article_dlsmjj = glob_article_category(request,'dlsmjj')
    article_qqsmjj = glob_article_category(request,'qqsmjj')
    article_by_gory = list(article_dlsmjj)+list(article_qqsmjj)
    return render_to_response('artical_list_smjj.html',locals())

def zzvip_list(request):
    article_srcp = glob_article_category(request,'srcp')
    article_zzvip = glob_article_category(request,'zzvip')
    article_by_gory = list(article_srcp)+list(article_zzvip)
    return render_to_response('artical_list_zzvip.html',locals())


def article_by_classname(classname):
    article = Article.objects.filter(className__title=classname)
    if len(article)>1:
        article  = article[0]
        #print(article_about)
    else:
        article = article[0]
        #print(article_about.title,article_about.content)
    return article

def about(request):
    article_about = article_by_classname(u'公司介绍')
    return render_to_response('artical_about.html',locals())

def company(request):
    article_company = Article.objects.get(title=u'操盘团队')
    return render_to_response('artical_company.html',locals())

def contacts(request):
    article_contacts = article_by_classname(u'联系我们')
    return render_to_response('artical_contacts.html',locals())

def services(request):
    article = article_by_classname(u'服务列表')
    return render_to_response('artical_services.html',locals())

def gsmap(request):
    article = article_by_classname(u'公司地图')
    return render_to_response('artical_gsmap.html',locals())
def ggfw(request):
    article = article_by_classname(u'广告服务')
    return render_to_response('artical_ggfw.html',locals())
def products(request):
    article = article_by_classname(u'产品与服务')
    return render_to_response('artical_products.html',locals())
def hzhb(request):
    article = article_by_classname(u'合作伙伴')
    return render_to_response('artical_hzhb.html',locals())
def flsm(request):
    article = article_by_classname(u'法律声明')
    return render_to_response('artical_flsm.html',locals())
def job(request):
    article = article_by_classname(u'人员招聘')
    return render_to_response('artical_job.html',locals())
"""
def side_berry(request):
    blueberry = ProductArticle.objects.filter(className__className=u'蓝莓苗木')
    return blueberry

def product_pagination(request):
    product_pag = ProductArticle.objects.all()
    return product_pag

def news_catagory(request,className):
    news_cata = Article.objects.filter(className__className=className)
    return news_cata

def index(request):
    sideberry = side_berry(request)
    product_pag = product_pagination(request)
    company_news = news_catagory(request,u'公司新闻')
    business_news = news_catagory(request,u'行业新闻')
    company_event = news_catagory(request,u'公司活动')
    website = Site.objects.all()
    return render_to_response('index2.html',locals())

def index2(request):
    sideberry = side_berry(request)
    product_pag = product_pagination(request)
    company_news = news_catagory(request,u'公司新闻')
    business_news = news_catagory(request,u'行业新闻')
    company_event = news_catagory(request,u'公司活动')
    website = Site.objects.all()
    return render_to_response('index2.html',locals())

def about(request):
    sideberry = side_berry(request)
    news_about = Article.objects.get(title=u'关于我们')
    return render_to_response('about.html',locals())

def company(request):
    sideberry = side_berry(request)
    news_company = Article.objects.get(title=u'蓝莓基地')
    return render_to_response('company.html',locals())

def contacts(request):
    sideberry = side_berry(request)
    news_contacts = Article.objects.get(title=u'联系我们')
    return render_to_response('contacts.html',locals())

def newscontent(request,id):
    sideberry = side_berry(request)
    news_by_id = Article.objects.get(id=id)
    return render_to_response('newscontent.html',locals())

def news(request):
    sideberry = side_berry(request)
    article = Article.objects.all()
    return render_to_response('newslist.html',locals())

def productcontent(request,id):
    sideberry = side_berry(request)
    product_by_id = ProductArticle.objects.get(id=id)
    return render_to_response('productcontent.html',locals())

def product(request):
    sideberry = side_berry(request)
    product_list = ProductArticle.objects.all()
    return render_to_response('productlist.html',locals())
"""