# sudo apt-get install libjpeg-dev
# pip install -I pillow
# http://stackoverflow.com/questions/8915296/python-image-library-fails-with-message-decoder-jpeg-not-available-pil

import os
from django import template
from django.db.models.fields.files import ImageFieldFile
from django.conf import settings
from PIL import Image, ImageEnhance
from watermarker import models

register = template.Library()


def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def make_watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    elif position == 'br':
        x = max(im.size[0] - mark.size[0], 0)
        y = max(im.size[1] - mark.size[1], 0)
        layer.paste(mark, (x, y))
    elif position == 'tr':
        x = max(im.size[0] - mark.size[0], 0)
        y = 0
        layer.paste(mark, (x, y))
    elif position == 'bl':
        x = 0
        y = max(im.size[1] - mark.size[1], 0)
        layer.paste(mark, (x, y))
    elif position == 'tl':
        x = y = 0
        layer.paste(mark, (x, y))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)


def get_path(url, root=settings.MEDIA_ROOT, url_root=settings.MEDIA_URL):
    """Makes a filesystem path from the specified URL"""

    if url.startswith(url_root):
        url = url[len(url_root):]  # strip media root url

    return os.path.normpath(os.path.join(root, url))


@register.filter
def watermark(url, wm_title):
    # to work not only with strings
    if isinstance(url, ImageFieldFile):
        if hasattr(url, 'url'):
            url = url.url

    print url
    basedir = '%s/watermarked' % os.path.dirname(url)
    base, ext = os.path.splitext(os.path.basename(url))

    # watermarked url for template
    wm_url = os.path.join(basedir, '%s%s' % (base, ext))
    # path to save watermarked img
    wm_path = get_path(wm_url)
    print wm_url, '\r\n'

    try:
        watermark = models.Watermark.objects.get(title=wm_title, is_active=True)
    except (models.Watermark.DoesNotExist, models.Watermark.MultipleObjectsReturned):
        return url

    # not to do more than we need
    if os.path.exists(wm_path) and not watermark.update_hard:
        return wm_url

    # create a folder for watermarks if needed
    wm_dir = os.path.dirname(wm_path)
    if not os.path.exists(wm_dir):
        os.makedirs(wm_dir)

    img_path = get_path(url)

    # this is a cap((
    if not os.path.exists(img_path):
        return url
    img = Image.open(img_path)


    mark = Image.open(watermark.mark.path)
    if watermark.position == models.Watermark.CUSTOM:
        x = watermark.x or 0
        y = watermark.y or 0
        position = (x, y)
    else:
        position = watermark.position

    opacity = watermark.opacity

    marked_img = make_watermark(img, mark, position, opacity)
    marked_img.save(wm_path)

    return wm_url