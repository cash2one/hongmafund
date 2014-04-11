#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import argparse ,os,sys,csv,json,re
sys.path.append('/home/ubuntu/project/hongmafund')
sys.path.append('/home/cbin/gits/hongmafund')
sys.path.append('/home/cbingo/webapps/hongmafund/hongmafund')

os.environ['DJANGO_SETTINGS_MODULE'] ='hongmafund.settings'

#from django.core.management import setup_environ
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hongmafund.settings")
#from hongmafund import settings
from django.conf import settings
from ems.models import *

#setup_environ(settings)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-i', dest='file' ,help= '需要转换csv文件' )
parser.add_argument('-n', dest='name', help= '根节点名称默认值为root)' ,default='data')
args = parser.parse_args()

filePath = args.file
objName = args.name

result = {}
escapeReg = re.compile('\"')

import datetime

def import_newscategory(filePath,*args):
    with open(filePath,'r') as file:
        reader = iter(csv.reader(file,quoting = csv.QUOTE_ALL))
        fields = next(reader)
        for index,line in enumerate(reader):
            result=({fields[k]:v for k,v in enumerate(line)})
            """insert NewsCategory csv data
               class2.csv 
            """
            newsCategory2 = NewsCategory(title=result['Class_Name'],keywords=result['Class_keywords'],description=result['Class_description'])
            newsCategory2.save()

def import_Article(filePath,*args):
    with open(filePath,'r') as file:
        reader = iter(csv.reader(file,quoting = csv.QUOTE_ALL))
        fields = next(reader)
        for index,line in enumerate(reader):
            result=({fields[k]:v for k,v in enumerate(line)})
            """insert Article csv data
               Info.csv 
            """
            #print(datetime.datetime.strptime(result['Info_Time'], "%m/%d/%Y %H:%M:%S"))
            article2 = Article(title=result['Info_Title'],className=NewsCategory.objects.get(title=result['Info_ClassId']),content=result['Info_Content'],article_time=datetime.datetime.strptime(result['Info_Time'], "%m/%d/%Y %H:%M:%S"),keywords=result['info_keywords'],summary=result['info_description'])
            article2.save()

def import_UserInfo(filePath,*args):
    with open(filePath,'r') as file:
        reader = iter(csv.reader(file,quoting = csv.QUOTE_ALL))
        fields = next(reader)
        for index,line in enumerate(reader):
            result=({fields[k]:v for k,v in enumerate(line)})
            """insert UserInfo csv data
                User.csv
            """
            from django.contrib.auth.models import User
            username = str(result['UserName'])
            #print(username)
            user = User.objects.create_user(username, result['Email'], '123456',)
            user.is_active = True
            user.is_staff = True
            user.userprofile.qq=result['QQ']
            user.userprofile.mobile=result['Mobile']
            user.userprofile.address=result['Add']
            user.userprofile.login_ip=result['LoginIP']
            user.userprofile.logins=result['logins']
            user.userprofile.user_type = u'MEMBER'
            user.userprofile.save()
            #user.user_permissions.add(u'auth.view_permission',u'auth.view_user',u'ems.change_userprofile',u'ems.view_article',u'ems.view_userprofile')
            user.save()
if __name__ == '__main__':
    import_newscategory('Class.csv')
    #import_Article('Info.csv')
    import_UserInfo('Users.csv')
