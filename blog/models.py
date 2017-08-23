# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import markdown
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    """
    此类为文章,textfield可以用来储存大量文本
    charfield默认情况下必须存入数据，所以blank=true则可以允许空值
    timezone Asia/Shanghai
    """
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)  # 摘要
    views = models.PositiveIntegerField(default=0)

    # 接下来为外键 https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，User是从 django.contrib.auth.models 导入的。
    # 这个模块是django专门用来处理网站用户注册、登录等流程。
    # User与文章是一对多，所以在此为ForeginKey
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 如果没有填写摘要excerpt
        if not self.excerpt:
            md = markdown.Markdown(extension=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        super(Post, self).save(*args, **kwargs)