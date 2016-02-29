# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/', views.about, name='about'),
                       url(r'^category/(?P<category_name>[\w\-]+)/$', views.category, name='category')
                       )
