# -*- coding: utf-8 -*-
from django.db import models
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class HmChart(models.Model):
    class Meta:
        verbose_name = u'股票期货净值管理'
        verbose_name_plural = u"股票期货净值管理"
        ordering = ['-chart_time']
    CHART_IN_HM_CHOICES = (
            ('STOCK', U'股票'),
            ('FUND', U'基金'),
    )
    chart_in_hm_choices = models.CharField(verbose_name=u'净值类型',choices=CHART_IN_HM_CHOICES,max_length=10,)
    chart_value = models.FloatField(verbose_name=u'值',max_length=20,null=True,blank=True,)
    chart_time = models.DateField(verbose_name=u'日期',blank=True,null=True,)

    def __unicode__(self):
        return self.chart_in_hm_choices

class HmadManager(models.Model):
    class Meta:
        verbose_name = u'首页广告图片管理'
        verbose_name_plural = u"广告图片管理"
        ordering = ['-ad_time']
    ad_title = models.CharField(verbose_name=u'标题',max_length=60,blank=True)
    source = models.CharField(verbose_name=u'来源',max_length=60,blank=True,null=True,default=u'http://www.simu88.com',)
    writer = models.CharField(verbose_name=u'作者',max_length=60,blank=True,null=True,default=u'www.simu88.com',)
    ad_time = models.DateTimeField(verbose_name=u'发布时间',blank=True,null=True,auto_now=True,auto_now_add=True)
    ad_Img = models.ImageField(verbose_name=u'广告图片',blank=True,upload_to='upimages',null=True,)
    ad_thumbnail = models.ImageField(verbose_name=u'广告缩略图',upload_to='thumbnail',blank=True,null=True)
    def __unicode__(self):
        return self.ad_title
    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.ad_Img:
            return
        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os
        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (238,210)
        PRODUCT_SIZE = (238,210)
        try:
            DJANGO_TYPE = self.ad_Img.file.content_type
            if DJANGO_TYPE == 'image/jpeg':
                PIL_TYPE = 'jpeg'
                FILE_EXTENSION = 'jpg'
            elif DJANGO_TYPE == 'image/jpg':
                PIL_TYPE = 'jpg'
                FILE_EXTENSION = 'jpg'
            elif DJANGO_TYPE == 'image/png':
                PIL_TYPE = 'png'
                FILE_EXTENSION = 'png'
                # Open original photo which we want to thumbnail using PIL's Image
            image = Image.open(StringIO(self.ad_Img.read()))
            #print('3333333333333333')
            # Convert to RGB if necessary
            # Thanks to Limodou on DjangoSnippets.org
            # http://www.djangosnippets.org/snippets/20/
            #
            # I commented this part since it messes up my png files
            #
            #if image.mode not in ('L', 'RGB'):
            #    image = image.convert('RGB')

            # We use our PIL Image object to create the thumbnail, which already
            # has a thumbnail() convenience method that contrains proportions.
            # Additionally, we use Image.ANTIALIAS to make the image look better.
            # Without antialiasing the image pattern artifacts may result.
            #image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
            #image.resize(THUMBNAIL_SIZE,Image.ANTIALIAS)
            img = image.resize(THUMBNAIL_SIZE,Image.ANTIALIAS)
            # Save the thumbnail
            temp_handle = StringIO()
            #image.save(temp_handle,PIL_TYPE)
            img.save(temp_handle, PIL_TYPE)
            temp_handle.seek(0)
            #print('2222222222222')
            ad_img = image.resize(PRODUCT_SIZE,Image.ANTIALIAS)
            temp_handle2 = StringIO()
            ad_img.save(temp_handle2,PIL_TYPE)
            temp_handle2.seek(0)
            # Save image to a SimpleUploadedFile which can be saved into
            # ImageField
            suf = SimpleUploadedFile(os.path.split(self.ad_Img.name)[-1],
                                     temp_handle.read(), content_type=DJANGO_TYPE)
            suf2 = SimpleUploadedFile(os.path.split(self.ad_Img.name)[-1],
                                      temp_handle2.read(), content_type=DJANGO_TYPE)
            # Save SimpleUploadedFile into image field
            print('aaatest')
            self.ad_thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
            self.ad_Img.save('%s.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf2, save=False)
        except:
            pass

    def save(self,*args, **kwargs):
        #self.slug = uuslug(self.title, instance=self,max_length=28,).replace('-','')
        #print('save------------')
        if not self.ad_Img:
            pass
        else:
            self.create_thumbnail()
        super(HmadManager, self).save(*args, **kwargs)
    def admin_thumbnail(self):
        return u'<img src="/media/thumbnail/%s" />' % (os.path.split(self.thumbnail.name)[-1])
    admin_thumbnail.short_description = u'广告图'
    admin_thumbnail.allow_tags = True
