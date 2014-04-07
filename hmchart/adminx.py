#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# Author: cbin
# mail: yu.cbin@gmail.com
#from django.contrib import admin

from hmchart.models import HmChart,HmadManager
import xadmin
from django.conf import settings


class HmChartAdmin(object):

    data_charts = {
        "stock_count": {'title': u"红马股票收益增长趋势图", "x-field": "chart_time", "y-field": ('chart_value'), "order": ('-chart_time',)},
        #"fund_count": {'title': u"期货收益增长趋势图", "x-field": "chart_time", "y-field": ('chart_value',), "order": ('-chart_time',)}
    }

    fields = ('chart_in_hm_choices','chart_value','chart_time',)
    #readonly_fields = ("registerdate",)
    list_filter = ('chart_in_hm_choices',)
    list_display = ('chart_in_hm_choices','chart_value','chart_time',)
    list_per_page = 10

class HmadManagerAdmin(object):
    #can_delete = False
    fields = ('ad_title','ad_Img','ad_thumbnail',)
    #readonly_fields = ("ad_title",)
    list_filter = ('ad_title','ad_time',)
    list_display = ('ad_title','ad_time','ad_Img','ad_thumbnail',)
    list_per_page = 10
xadmin.site.register(HmChart, HmChartAdmin)
xadmin.site.register(HmadManager,HmadManagerAdmin)