Watermarker
==========
Watermarker - это тулза для легкого, почти ванильного создания водяных знаков на картинках вашего проекта. Редактирование 
положения водяных знаков происходит в админке. Под водяным знаком понимается картинка, поддержки текста пока нет.
Работает с Jinja2 (требуется django-jinja).

## Проверялось с

* Python 2.7
* Django 1.6, 1.7, 1.8

## Подключение к проекту
Как сабмодуль, поддержка pip в планах:    

    git submodule add https://github.com/Skycker/watermarker
  
## Настройка  
Добавляем приложение в `INSTALLED_APPS`:  

    INSTALLED_APPS = (
        ...
        'watermarker',
        ...
    )

*Для Django < 1.7*

    ./manage.py syncdb
    
*Для Django >= 1.7*

В проекте приложены миграции

    ./manage.py migrate

## WorkFlow  
В панели администратора появляется модель `Watermrks`. Заходим создаем новый объект, заполняем. Особенно удобно при 
необходимости ставить разные возяные знаки на страницах (в данном случае просто создаем несколько записей 
в таблице `Watermrks`)

Маленькие особенности:  
    1. Заголовок (Title) набираем по-английски, он нам понадобится позже.  
    2. Если в графе Позиция (Position) выбираем местоположение ваодяного знака
    3. Для позиций по углам можно заполнить отступы по осям Х и У
    4. В штатном режиме либа не перерисовывает уже созданные ватермарки. Но если очень хочется или поменялись настройки отображения знака, то
        пункт Update hard вам поможет. Если он установлен в True, то при рендеринге страницы будут всегда перерисовываться ватермарки.
        Не забудьте снять флаг после применнеия изменений, ибо производительность.  
    5. Графа Is active работает как обычно. Это способ в один клин отключить ватермарку. При этом не нужно идти в код и что-то там менять

Водяные знаки накладываются в шаблонах. 

**Классический шаблонизатор Django**

Импортируем и применяем шаблонный фильтр:  

    {% load watermarks %}
    
    <img src="{{ image.img.url|watermark:'wm_title' }}" alt="{{ image.title }}">
    wm_title - имя для ватермарка, которое писали в графу Заголовок в админке.  

Способ работы с `easy_thumbnails`:  

    {% load thumbnail %}  
    {% load watermarks %}     
    
    {% thumbnail image.img|watermark:'wm_title' 160x160 as thumb %}
    <img src="{{ thumb.url|get_url_safe }}" alt="{{ image.title }}"/> 

Если передавать как аргумент фильтру строку с названием ватермарка, то каждый раз, для каждой фотки приходится делать  
запрос в БД, чтобы достать данные о водяном знаке. В целях производительности можно передать фильтру объект кдасса 
`Watermark`, который предварительно один раз вычислить во вьюхе. Лучше использовать именно этот режим

    Во views.py:
    from watermarker.models import Watermark
    
    def get_context_data(self, **kwargs):
        cd = super(Index, self).get_context_data()
        cd['wm'] = Watermark.objects.get(title='wm_title')
        return cd
    
    В шаблоне:
    <img src="{{ image.img.url|watermark:wm }}" alt="{{ image.title }}">

    {% thumbnail image.img|watermark:wm 160x160 as thumb %}
    <img src="{{ thumb.url|get_url_safe }}" alt="{{ image.title }}"/>

Рядом с файлами создается папка `watermarked` и изображения с водяными знаками склыдвываются туда. 
Так что исходные картинки не теряются. Если в какой-то момент водяные знаки надоели, то их можно отключить, 
убрав галочку Is active. При этом менять что-то в коде нет необходимости

**Поддержка Jinja2**

Необходима предварительная установка `djngo-jinja`
    
    <img src="{{ image.img.url|watermark('wm_title') }}" alt="{{ image.title }}">
    <img src="{{ thumbnail(image.img|watermark('wm_title'), size=(160, 160))|get_url_safe() }}" alt="{{ image.title }}"/>
    
    <img src="{{ image.img.url|watermark(wm) }}" alt="{{ image.title }}">
    <img src="{{ thumbnail(image.img|watermark(wm), size=(160, 160))|get_url_safe() }}" alt="{{ image.title }}"/>

## Требования
Для нормального функционирования требуется PIL и вся толпа пакетов для него.

Если совсем не работает, то возможно не хватает пакетов для PIL:

    apt-get install libjpeg-dev
    http://stackoverflow.com/questions/8915296/python-image-library-fails-with-message-decoder-jpeg-not-available-pil


