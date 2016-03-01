# django的练习与学习笔记

### 1、url 映射
> /rango/   主页
/rango/about/  关于
/rango/category/<category_name>/   指向每个category的目录视图
/rango/etc/  为将来功能流出etc

### 2、建表
|category table||
|----|----|
|field|type|
|name|str|
|views|int|
|likes|int|

|page table||
|---|---|
|field|type|
|category|FK|
|title|str|
|url|URL|
|views|int|

### 3、一些基础操作
1、安装python 图形库  
```bash
pip install pillow
```
2、查看当前环境下依赖列表
```bash
pip list
```
3、分享包列表
```bash
pip freeze > requirements.txt
```
4、根据包列表批量安装依赖
```bash
pip install -r requirements.txt
```
### 4、创建虚拟环境
创建虚拟环境首先需要安装两个包
```bash
pip install virtualenv
pip install virtualenvwrapper
```
第二个包是为了简化操作的
mac系统下需要启动这个脚本
```bash
source virtualenvwrapper.sh #每次都要执行这个命令
```
win下需要另外安装一个脚本
```bash
pip install virtualenvwrapper-win
```
以上搞定后就可以创建虚拟环境了
```bash
mkvirtualenv somename
lsvirtualenv  #这个命令列出环境列表
```
然后启动虚拟环境
```bash
workon somename
```

### 5、编码实现url映射
首先是在应用目录下需要自己新建一个urls.py
然后对这个应用下的url进行配置
```python
from django.conf.urls import pattern, url
from tango import views

urlpattern = pattern('',url(r'^index/',views.index,name='index'))
```
然后在项目的的urls.py中包含上面配置好的url
```python
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rango/', include('rango.urls'))
]
```
这时候的访问地址为
> http://127.0.0.1:8000/tango/index/

参数化的url映射
```python
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.category, name='category'),)  # New!
    # 这里的P用来传参   这里的参数名应该跟view中接受参数的参数名相同
```

### 6、静态文件服务配置
首先在settings中设置
```python
STATIC_PATH = os.path.join(BASE_DIR,'static')

STATIC_URL = '/static/' # You may find this is already defined as such.

STATICFILES_DIRS = [
    STATIC_PATH,
]
```
然后模版中引入静态文件如下
```html
<!DOCTYPE html>
{% load static %}
<html>
    <head>
        <title>Rango</title>
        <link rel="stylesheet" href="{% static "css/base.css" %}" /> <!-- CSS -->
        <script src="{% static "js/jquery.js" %}"></script> <!-- JavaScript -->
    </head>
    <body>
        <h1>Including Static Media</h1>
        <img src="{% static "images/rango.jpg" %}" alt="Picture of Rango" /> <!-- Images -->
    </body>
</html>
```
然后在urls.py中加入下面的代码
```python
from django.conf import settings # New Import
from django.conf.urls.static import static # New Import


if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
### 7、媒体文件配置服务
首先修改urls
```python
# At the top of your urls.py file, add the following line:
from django.conf import settings

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
```
然后修改setting
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Absolute path to the media directory
```

> 备注：以上不论是静态文件还是静态媒体文件，static目录和media目录都放在根目录下跟templates和项目文件夹同一目录

### 8、模型和数据库
在setting中进行数据库的配置，如果是sqllite数据库只需要制定文件存储的目录：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
而如果是mysql数据库需要配置USER,PASSWORD,HOST和PORT等关键字。
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'books',    #数据库名称
        'USER': 'root',     #数据库用户名
        'PASSWORD': '',     #数据库密码
        'HOST': '',         #数据库主机，留空默认为localhost
        'PORT': '3306',     #数据库端口
    }
}
```
在models.py中创建django的模型，一个模型对应一个数据表，设计好的模型可以通过执行django的命令来自动创建数据表。
例如：
```python
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.title
```
不需要手动设定主键，主键会自动创建好
常见的字段有:
> * CharField,存储字符数据的字段(例如字符串).max_length提供了最大长度。
* URLField,和CharField一样,但是它存储资源的URL.你也可以使用max_length参数。
* 'IntegerField',存储整数。
* DateField,存储Python的datetime.date。

Django也提供了连接模型/表的简单机制.这个机制封装在3个字段里,如下.
> * ForeignKey, 创建1对多关系的字段类型.
* OneToOneField,定义一个严格的1对1关系字段类型.
* ManyToManyFeild,当以多对多关系字段类型.

创建并同步数据模型，然后用如下命令设置数据库
```bash
python manage.py migrate
```
然后创建数据库超级管理员：
```bash
python manage.py createsuperusersa
```
当修改过模型的时候，通过makemigrations进行修改：
```bash
python manage.py makemigrations
```
然后运行
```bash
python manage.py migrate
```
### 9、简单设置管理界面
打开对应app下的admin.py  可以对自定义的模型进行注册
```python
from django.contrib import admin
from rango.models import Category, Page

#定制page页面的管理界面
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url') #定制三个字段

admin.site.register(Category)
admin.site.register(Page, PageAdmin) #绑定定制的页面
```
然后进入admin就可以看到相应的表了


### 10、部署参考资料
http://blog.csdn.net/a359680405/article/details/43113039