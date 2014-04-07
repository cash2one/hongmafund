#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import datetime,os,sys,random

sys.path.append('/home/cbin/gits/hongmafund')
sys.path.append('/home/cbingo/webapps/hongmafund/hongmafund')
os.environ['DJANGO_SETTINGS_MODULE'] ='hongmafund.settings'

#from django.core.management import setup_environ
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hongmafund.settings")
#from hongmafund import settings
from django.conf import settings
from hmchart.models import *

#HmChart(chart_in_hm_choices=u'STOCK',chart_time=datetime.date(2002,1,15),chart_value=1.0).save()

def hmchart_data(choice,start_year,end_year):
    """
    随机递增净值数据，递增区间：0.03-0.15
    :param choice: 净值类型
    :param start_year:　开始年份
    :param end_year:　结束年
    :return:
    """
    value = 1.0
    for y in range(start_year,end_year):
        for m in range(1,13):
            value += value*random.uniform(-0.06,0.15)
            print(y,m,value)
            HmChart(chart_in_hm_choices=choice,chart_time=datetime.date(y,m,15),chart_value=value).save()

def month_crontab():
    """
    每月15号 早上１０点，自动递增净值数据，递增区间：0.03-0.15
    服务器执行crontab 0 10 15 * * python2.7 import chart.py
    """
    from django.db.models import Max
    stock_value = HmChart.objects.filter(chart_in_hm_choices=u'STOCK').aggregate(Max('chart_value'))['chart_value__max']+random.uniform(0.3,0.15)
    fund_value = HmChart.objects.filter(chart_in_hm_choices=u'FUND').aggregate(Max('chart_value'))['chart_value__max']+random.uniform(0.3,0.15)

    HmChart(chart_in_hm_choices=u'STOCK',chart_time=datetime.datetime.now(),chart_value=stock_value).save()
    HmChart(chart_in_hm_choices=u'FUND',chart_time=datetime.datetime.now(),chart_value=fund_value).save()

def call_hmchart_data():
    stock_year=2006
    fund_year=2002
    end_year = 2015
    stock_choice = u'STOCK'
    fund_choice = u'FUND'
    hmchart_data(fund_choice,fund_year,end_year)
    hmchart_data(stock_choice,stock_year,end_year)
if __name__ == '__main__':
    call_hmchart_data()
    #month_crontab()
