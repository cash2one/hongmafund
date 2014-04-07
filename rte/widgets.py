__author__ = 'cbin'
#coding=utf8
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import RadioFieldRenderer, RadioInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.translation import ugettext as _
from itertools import chain


class Ueditor(forms.Textarea):

    def __init__(self,attrs={}):
        super(Ueditor,self).__init__(attrs)
    def render(self,name,value,attrs=None):
    # rendered = super(Ueditor,self).render(name,value,attrs)
        context = {
            'name':name,
            'STATIC_URL':settings.STATIC_URL,
            'value':value,
            }

        return  mark_safe(render_to_string('widgets/ueditor.html',context))
