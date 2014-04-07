# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
from DjangoUeditor.models import UEditorField
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class UserProfile(models.Model):
    class Meta:
        verbose_name = u'会员信息设置'
        verbose_name_plural = u"会员管理"
    USER_CHOICES = (
        ('MEMBER', U'普通会员'),
        ('HIGHMEMBER', U'高级会员'),
        ('PAYMEMBER', U'付费会员'),
        ('SPECIALTY', U'尊享VIP会员'),
    )
    user = models.OneToOneField(User,verbose_name=u'用户名',unique=True,)
    qq=models.CharField(verbose_name=u'ＱＱ',max_length=80,blank=True,null=True)
    user_type=models.CharField(verbose_name=u'用户级别',max_length=80,blank=True,null=True,choices=USER_CHOICES,)
    #taobao=models.CharField(max_length=80,blank=True,null=True)
    #email=models.CharField(verbose_name=u'邮箱',max_length=80,blank=True,null=True,default=User.email)
    phone=models.CharField(max_length=80,blank=True,null=True)
    mobile=models.CharField(verbose_name=u'手机号',max_length=80,blank=True,null=True)
    address=models.CharField(verbose_name=u'地址',max_length=80,blank=True,null=True)
    login_ip=models.CharField(verbose_name=u'登陆IP',max_length=80,blank=True,null=True,)
    logins = models.IntegerField(verbose_name=u'登陆次数',max_length=80,blank=True,null=True,default=0,)
    def __unicode__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

# Signal while saving user
from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)

class NewsCategory(models.Model):
    class Meta:
        verbose_name = u'栏目设置'
        verbose_name_plural = u"栏目管理"
        #app_label = u"私募机构信息"
        #db_table = 'ems_newscategory'
    slug = models.CharField(verbose_name=u'title',max_length=50,blank=True,null=True)
    title = models.CharField(verbose_name=u'栏目名称',max_length=50,blank=True,null=True)
    keywords = models.CharField(verbose_name=u'Keywords',max_length=150,blank=True,null=True)
    description = models.CharField(verbose_name=u'Description',max_length=200,blank=True,null=True)

    def __unicode__(self):
        return self.title
"""
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self,max_length=18,).replace('-','')
        super(NewsCategory, self).save(*args, **kwargs)
"""
class Article(models.Model):
    class Meta:
        verbose_name = u'信息管理'
        verbose_name_plural = u"信息管理"
        ordering = ['-article_time']
    title = models.CharField(verbose_name=u'标题',max_length=100,blank=True)
    keywords = models.CharField(verbose_name=u'Keywords',max_length=500,blank=True,null=True,default=u"期货-期货实盘账户-期货私募基金-期货投资-期货操盘-期货资金曲线-期货操盘手",)
    summary = models.CharField(verbose_name=u'Description',max_length=500,blank=True,null=True,default=u"牢记网址：www.simu88.com;只做期货的代理操盘;股票代理操盘，分成条款：季度结算四六分",)
    className = models.ForeignKey(NewsCategory,verbose_name=u'所属栏目')
    slug = models.CharField(verbose_name=u'自定义URL',max_length=200,blank=True,null=True)
    source = models.CharField(verbose_name=u'来源',max_length=60,blank=True,null=True,default=u'http://www.simu88.com',)
    writer = models.CharField(verbose_name=u'作者',max_length=60,blank=True,null=True,default=u'www.simu88.com',)
    headline = models.CharField(verbose_name=u'头条新闻',max_length=60,blank=True,null=True,)
    hightlight = models.CharField(verbose_name=u'标题醒目',max_length=60,blank=True,null=True,)
    hints = models.CharField(verbose_name=u'点击数',max_length=60,blank=True,null=True,)
    article_time = models.DateTimeField(verbose_name=u'发布时间',blank=True,null=True,)#auto_now=True,auto_now_add=True)
    productImg = models.ImageField(verbose_name=u'产品图片',blank=True,upload_to='upimages',null=True,)
    thumbnail = models.ImageField(verbose_name=u'产品缩略图',upload_to='thumbnail',blank=True,null=True)
    content = UEditorField(u'内容',max_length=1000,width=250,height=300,default=u'请键入产品描述',imagePath="upimages/",imageManagerPath="",toolbars='full',options={"elementPathEnabled":True},filePath='upload',blank=True)
    added_by = models.ForeignKey(User,verbose_name=u"所属用户",null=True,blank=True)
    def __unicode__(self):
        return self.title
    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.productImg:
            return
        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os
        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (176,120)
        PRODUCT_SIZE = (284,188)
        try:
            DJANGO_TYPE = self.productImg.file.content_type
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
            image = Image.open(StringIO(self.productImg.read()))
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

            productimg = image.resize(PRODUCT_SIZE,Image.ANTIALIAS)
            temp_handle2 = StringIO()
            productimg.save(temp_handle2,PIL_TYPE)
            temp_handle2.seek(0)
            # Save image to a SimpleUploadedFile which can be saved into
            # ImageField
            suf = SimpleUploadedFile(os.path.split(self.productImg.name)[-1],
                                     temp_handle.read(), content_type=DJANGO_TYPE)
            suf2 = SimpleUploadedFile(os.path.split(self.productImg.name)[-1],
                                      temp_handle2.read(), content_type=DJANGO_TYPE)
            # Save SimpleUploadedFile into image field
            self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
            self.productImg.save('%s.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf2, save=False)
        except:
            pass

    def save(self,*args, **kwargs):
        #self.slug = uuslug(self.title, instance=self,max_length=28,).replace('-','')
        if not self.productImg:
            pass
        else:
            self.create_thumbnail()
        super(Article, self).save(*args, **kwargs)
    def admin_thumbnail(self):
        return u'<img src="/media/thumbnail/%s" />' % (os.path.split(self.thumbnail.name)[-1])
    admin_thumbnail.short_description = u'产品缩略图'
    admin_thumbnail.allow_tags = True
"""
    def save(self,*args, **kwargs):
        self.slug = uuslug(self.title, instance=self,max_length=28,).replace('-','')
        super(Article, self).save(*args, **kwargs)
"""
"""

class ProductCategory(models.Model):
    class Meta:
        verbose_name = u'产品种类管理'
        verbose_name_plural = u"产品种类管理"
    className = models.CharField(verbose_name=u'产品种类名称',max_length='30',blank=True)
    slug = models.CharField(verbose_name=u'自定义URL',max_length=200,blank=True,null=True)
    title = models.CharField(verbose_name=u'产品种类标题',max_length=50,blank=True,null=True)
    keywords = models.CharField(verbose_name=u'产品种类关键词',max_length=50,blank=True,null=True)
    description = models.CharField(verbose_name=u'产品种类描述',max_length=200,blank=True,null=True)
    def __unicode__(self):
        return self.className
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.className, instance=self,max_length=28,).replace('-','')
        super(ProductCategory, self).save(*args, **kwargs)

class ProductArticle(models.Model):
    class Meta:
        verbose_name = u'产品管理'
        verbose_name_plural = u"产品管理"
        ordering = ['-productime']
    title = models.CharField(verbose_name=u'产品名称',max_length=60,blank=True)
    keywords = models.CharField(verbose_name=u'产品关键词',max_length=60,blank=True,null=True,)
    className = models.ForeignKey(ProductCategory,verbose_name=u'产品种类')
    slug = models.CharField(verbose_name=u'产品URL',max_length=200,blank=True,null=True)
    source = models.CharField(verbose_name=u'来源',max_length=60,blank=True,null=True,default=u'http://www.xixiguonong.com',)
    writer = models.CharField(verbose_name=u'作者',max_length=60,blank=True,null=True,default=u'西溪果农',)
    headline = models.CharField(verbose_name=u'产品推荐',max_length=60,blank=True,null=True,)
    summary = models.CharField(verbose_name=u'产品简介',max_length=60,blank=True,null=True,)
    hints = models.CharField(verbose_name=u'点击数',max_length=60,blank=True,null=True,)
    productime = models.DateTimeField(verbose_name=u'产品发布时间',blank=True,null=True,auto_now=True,auto_now_add=True)
    productImg = models.ImageField(verbose_name=u'产品图片',blank=True,upload_to='upimages',null=True,)
    thumbnail = models.ImageField(verbose_name=u'产品缩略图',upload_to='thumbnail',blank=True,null=True)
    content = UEditorField(u'内容',height=350,width=800,default=u'请键入产品描述',imagePath="upimages/",imageManagerPath="",toolbars='full',options={"elementPathEnabled":True},filePath='upload',blank=True)
    def __unicode__(self):
        return self.title
    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.productImg:
            return
        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os
        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (176,120)
        PRODUCT_SIZE = (284,188)
        try:
            DJANGO_TYPE = self.productImg.file.content_type
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
            image = Image.open(StringIO(self.productImg.read()))
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

            productimg = image.resize(PRODUCT_SIZE,Image.ANTIALIAS)
            temp_handle2 = StringIO()
            productimg.save(temp_handle2,PIL_TYPE)
            temp_handle2.seek(0)
            # Save image to a SimpleUploadedFile which can be saved into
            # ImageField
            suf = SimpleUploadedFile(os.path.split(self.productImg.name)[-1],
                                    temp_handle.read(), content_type=DJANGO_TYPE)
            suf2 = SimpleUploadedFile(os.path.split(self.productImg.name)[-1],
                                     temp_handle2.read(), content_type=DJANGO_TYPE)
            # Save SimpleUploadedFile into image field
            self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
            self.productImg.save('%s.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf2, save=False)
        except:
            pass

    def save(self,*args, **kwargs):
        self.slug = uuslug(self.title, instance=self,max_length=28,).replace('-','')
        if not self.productImg:
            pass
        else:
            self.create_thumbnail()
        super(ProductArticle, self).save(*args, **kwargs)
    def admin_thumbnail(self):
        return u'<img src="/media/thumbnail/%s" />' % (os.path.split(self.thumbnail.name)[-1])
    admin_thumbnail.short_description = u'产品缩略图'
    admin_thumbnail.allow_tags = True
"""