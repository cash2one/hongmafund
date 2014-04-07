# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpRequest
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response,get_object_or_404,get_list_or_404,RequestContext
from django.contrib.sites.models import Site, RequestSite, get_current_site
from hmchart.models import *
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.shortcuts import render_to_response
import random
import datetime
import time
from nvd3 import lineChart,lineWithFocusChart
import calendar


def index_linechart(request):
    """
    lineChart page
    """
    today = datetime.date.today()
    year = today.year
    stock_list = HmChart.objects.filter(chart_in_hm_choices=u'STOCK',chart_time__year=year)
    xdata = [int(calendar.timegm(t.chart_time.timetuple()))*1000 for t in stock_list]
    ydata = [float("%.2f"%v.chart_value) for v in stock_list]

    chart = lineChart(name='lineChart', container='lineChart',height=400, width=400, x_is_date=True, x_axis_format="%d %b %Y")
    #xdata = [1365026400000000, 1365026500000000, 1365026600000000]
    #ydata = [-6, 5, -1]
    #tooltip_str = "'<center><b>'+key+'</b></center>' + y + ' 增长 ' + x;"

    extra_serie = {"tooltip": {"y_start": "净值", "y_end": ""},
               "date_format": "%Y年%m月%d日",
               #"tooltip_str": tooltip_str,
               }
    chart.add_serie(name=u"股票净值", y=ydata, x=xdata, extra=extra_serie,)
    chart.buildhtml()
    chart_html = chart.jschart
    #--------------------------------------------------------------
    chart2 = lineChart(name='lineChart2',container='lineChart2',height=400, width=400, x_is_date=True, x_axis_format="%d %b %Y")
    fund_list = HmChart.objects.filter(chart_in_hm_choices=u'FUND',chart_time__year=year)
    xdata2 = [int(calendar.timegm(t.chart_time.timetuple()))*1000 for t in fund_list]
    ydata2 = [float("%.2f"%v.chart_value) for v in fund_list]
    #xdata2 = [1365988400000000, 1365026500000000, 1365026600000000]
    #ydata2 = [8, 5, 3]

    extra_serie2 = {"tooltip": {"y_start": "净值", "y_end": ""},
                   "date_format": "%Y年%m月%d日"}
    chart2.add_serie(name=u"期货净值", y=ydata2, x=xdata2, extra=extra_serie2)
    chart2.buildhtml()
    chart_html2 = chart2.jschart
    adimg = HmadManager.objects.all()
    return render_to_response('nvd3/index.html', locals())


def index_chart(request):
    """
    lineChart page
    """
    today = datetime.date.today()
    year = today.year
    stock_list = HmChart.objects.filter(chart_in_hm_choices=u'STOCK',chart_time__year=year)
    xdata = [int(calendar.timegm(t.chart_time.timetuple()))*1000 for t in stock_list]
    ydata = [float("%.2f"%v.chart_value) for v in stock_list]

    chart = lineChart(name='lineChart', container='lineChart',height=400, width=400, x_is_date=True, x_axis_format="%d %b %Y")
    #xdata = [1365026400000000, 1365026500000000, 1365026600000000]
    #ydata = [-6, 5, -1]
    #tooltip_str = "'<center><b>'+key+'</b></center>' + y + ' 增长 ' + x;"

    extra_serie = {"tooltip": {"y_start": "净值", "y_end": ""},
                   "date_format": "%Y年%m月%d日",
                   #"tooltip_str": tooltip_str,
    }
    chart.add_serie(name=u"股票净值", y=ydata, x=xdata, extra=extra_serie,)
    chart.buildhtml()
    chart_html = chart.jschart
    #--------------------------------------------------------------
    chart2 = lineChart(name='lineChart2',container='lineChart2',height=400, width=400, x_is_date=True, x_axis_format="%d %b %Y")
    fund_list = HmChart.objects.filter(chart_in_hm_choices=u'FUND',chart_time__year=year)
    xdata2 = [int(calendar.timegm(t.chart_time.timetuple()))*1000 for t in fund_list]
    ydata2 = [float("%.2f"%v.chart_value) for v in fund_list]
    #xdata2 = [1365988400000000, 1365026500000000, 1365026600000000]
    #ydata2 = [8, 5, 3]

    extra_serie2 = {"tooltip": {"y_start": "净值", "y_end": ""},
                    "date_format": "%Y年%m月%d日"}
    chart2.add_serie(name=u"期货净值", y=ydata2, x=xdata2, extra=extra_serie2)
    chart2.buildhtml()
    chart_html2 = chart2.jschart
    adimg = HmadManager.objects.all()
    return chart_html,chart_html2

def linewithfocuschart(request,choice):
    """
    linewithfocuschart page
    """
    CHART_CHOICES = {
            'stock':U'STOCK',
            'fund':U'FUND',
    }
    CHART_CHOICES_NAME = {
            'stock':U'红马股票净值',
            'fund':U'红马期货净值',
    }
    chart_name = CHART_CHOICES_NAME.get(choice)
    choice2 = CHART_CHOICES.get(choice)
    
    print(chart_name)
    chart = lineWithFocusChart(name='lineWithFocusChart', x_is_date=True, x_axis_format="%d %b %Y")
    stock_list = HmChart.objects.filter(chart_in_hm_choices=choice2)
    xdata = [int(calendar.timegm(t.chart_time.timetuple()))*1000 for t in stock_list]
    ydata = [float("%.2f"%v.chart_value) for v in stock_list]

    extra_serie = {"tooltip": {"y_start": "净值", "y_end": ""},"date_format": "%Y年%m月%d日"}
    chart.add_serie(name=chart_name, y=ydata, x=xdata, extra=extra_serie)
    chart.buildhtml()    
    chart_html = chart.jschart
    return render_to_response('artical_hmcharts.html', locals())

def admanager(request):
    ad1 = HmadManager.objects.get(ad_title='index_images1')
    ad2 = HmadManager.objects.get(ad_title='index_images2')
    return ad1,ad2