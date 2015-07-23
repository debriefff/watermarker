Watermarker
==========
Watermarker is a tool for easy creating watermarks in you Django project. Editing takes place in the admin panel. 
Watermarker put image (watermark) upon content images, text based watermarks support coming soon. 

It works with Jinja2 (django-jinja required)

## Tested with

* Python 2.7
* Django 1.6, 1.7, 1.8

## Install

Via pip:

    pip install git+https://github.com/Skycker/watermarker@master

## Setup 
 
Add app name in  `INSTALLED_APPS`:  

    INSTALLED_APPS = (
        ...
        'watermarker',
        ...
    )

*For Django < 1.7*

    ./manage.py syncdb
    
*For Django >= 1.7*

There are migrations in project

    ./manage.py migrate

## WorkFlow  

After installation model `Watermarks` will appear in admin panel. Go there, create a new instance, edit it. It's very 
useful if we need use different watermarks at site pages (this way just create several `Watermark`-instances)

Little features:  
    1. Field `Title` indicates our watermark ( `wm_title` for example, we will use it a bit later)   
    2. Upload watermark image (there is an example in repo to test)  
    3. In `Position` choose place for watermarks  
    4. For positions at corners you can tune X and Y indent  
    5. Content images get their watermarks when page loads for the first time. By default the library does not redraw   
       already created watermarks. If you need change it use `Update hard`. If it is `True` watermarker change   
       watermarks for images every time when page loads. Be accurate! It decrease performance very much  
    6. `Is active` is an easy way to switch watermark off. There is no necessity to change code  

[Admin interface example](https://habrastorage.org/files/0c7/14b/6eb/0c714b6eba8f424e94e63fe4429e52e7.png)

Watermarks are set to images in templates. 

**Classic Django template engine**

Import and use template filter:  

    {% load watermarks %}
    
    <img src="{{ image.img.url|watermark:'wm_title' }}" alt="{{ image.title }}">
    wm_title - имя для ватермарка, которое писали в графу Заголовок в админке.  

The way to work with `easy_thumbnails`:  

    {% load thumbnail %}  
    {% load watermarks %}     
    
    {% thumbnail image.img|watermark:'wm_title' 160x160 as thumb %}
    <img src="{{ thumb.url|get_url_safe }}" alt="{{ image.title }}"/> 

If provide watermark name in filter every time for every image system will make query to `Watermark` table in database
to take data. To increase performance you can provide calculated in view instance of Watermark class. We recommend use 
this mode if it is possible.

    In views.py:
    from watermarker.models import Watermark
    
    def get_context_data(self, **kwargs):
        cd = super(Index, self).get_context_data()
        cd['wm'] = Watermark.objects.get(title='wm_title')
        return cd
    
    In template:
    <img src="{{ image.img.url|watermark:wm }}" alt="{{ image.title }}">

    {% thumbnail image.img|watermark:wm 160x160 as thumb %}
    <img src="{{ thumb.url|get_url_safe }}" alt="{{ image.title }}"/>

Images with watermarks are kept in folder `watermark` which is created in your media directory.

> original images are not deleted!


**Jinja2 support**

`djngo-jinja` is required
    
    <img src="{{ image.img.url|watermark('wm_title') }}" alt="{{ image.title }}">
    <img src="{{ thumbnail(image.img|watermark('wm_title'), size=(160, 160))|get_url_safe() }}" alt="{{ image.title }}"/>
    
    <img src="{{ image.img.url|watermark(wm) }}" alt="{{ image.title }}">
    <img src="{{ thumbnail(image.img|watermark(wm), size=(160, 160))|get_url_safe() }}" alt="{{ image.title }}"/>

## Localisation

By default:  
    * English  
    * Russian  

## Requirements

For stable fork `pillow` is required.

If smth wrong this list can possibly help:

    apt-get install libjpeg-dev
    http://stackoverflow.com/questions/8915296/python-image-library-fails-with-message-decoder-jpeg-not-available-pil


