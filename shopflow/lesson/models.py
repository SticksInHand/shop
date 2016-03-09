from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     uid = models.CharField(max_length=6)
#     tel = models.CharField(max_length=11)
#     website = models.URLField(blank=True)
#     isauthor = models.IntegerField()
#     picture = models.ImageField(upload_to='profile_images', blank=True)
#
#     def __unicode__(self):
#         return self.user.username


class Book(models.Model):
    bookname = models.CharField(max_length=128, unique=True)
    bookid = models.CharField(max_length=6, unique=True)
    uid = models.CharField(max_length=6)
    booktime = models.DateField(auto_created=True)
    bookcategory = models.CharField(max_length=50)

    def __unicode__(self):
        return self.bookname


class Article(models.Model):
    artname = models.CharField(max_length=128, unique=True)
    artid = models.CharField(max_length=6, unique=True)
    artcontent = models.TextField()
    arttime = models.DateField(auto_created=True)
    bookid = models.CharField(max_length=6)

    def __unicode__(self):
        return self.artname
