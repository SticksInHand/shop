# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from lesson import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^lesson_detail/', views.lesson_detail, name='lesson_detail'),
                       # url(r'^add_category/$', views.add_category, name='add_category'),
                       # url(r'^category/(?P<category_name>[\w\-]+)/$', views.category, name='category')
                       )