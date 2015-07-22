# coding: utf-8
import os
import urllib
from logging import error

from django.db.models.fields.files import ImageFieldFile, ImageField
from django.conf import settings
from PIL import Image, ImageEnhance

from watermarker import models


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


def make_watermark(im, mark, position, opacity=1, shift=(0, 0)):
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
        x = max(im.size[0] - mark.size[0], 0) - shift[0]
        y = max(im.size[1] - mark.size[1], 0) - shift[1]
        layer.paste(mark, (x, y))
    elif position == 'tr':
        x = max(im.size[0] - mark.size[0], 0) - shift[0]
        y = 0 + shift[1]
        layer.paste(mark, (x, y))
    elif position == 'bl':
        x = 0 + shift[0]
        y = max(im.size[1] - mark.size[1], 0) - shift[1]
        layer.paste(mark, (x, y))
    elif position == 'tl':
        x = 0 + shift[0]
        y = 0 + shift[1]
        layer.paste(mark, (x, y))
    else:
        layer.paste(mark, (0, 0))
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)


def get_path(url):
    """Makes a filesystem path from the specified URL"""

    if url.startswith(settings.MEDIA_URL):
        root = settings.MEDIA_ROOT
    else:
        root = settings.STATIC_ROOT

    url = url.replace(settings.MEDIA_URL, '').replace(settings.STATIC_URL, '')
    url = urllib.unquote(url).decode("utf8")
    return os.path.normpath(os.path.join(root, url))


def make_iff_instance(path):
    """ Returns ImageFieldFile for provided image path """

    return ImageFieldFile(instance=None, field=ImageField(), name=path)


def watermark(url, wm):
    # return usual url(string) or ImageFieldFile
    result_as_iff = False

    if isinstance(wm, models.Watermark):
        watermark = wm
    else:
        try:
            watermark = models.Watermark.objects.get(title=wm, is_active=True)
        except (models.Watermark.DoesNotExist, models.Watermark.MultipleObjectsReturned):
            return url

    # to work not only with strings
    if isinstance(url, ImageFieldFile):
        result_as_iff = True
        if hasattr(url, 'url'):
            url = url.url
        else:
            return url

    basedir = '%s/watermarked' % os.path.dirname(url)
    base, ext = os.path.splitext(os.path.basename(url))

    # watermarked url for template
    wm_url = os.path.join(basedir, '%s%s' % (base, ext))
    # path to save watermarked img
    wm_path = get_path(wm_url)

    # not to do more than we need
    if os.path.exists(wm_path) and not watermark.update_hard:
        if result_as_iff:
            return make_iff_instance(wm_path)
        return wm_url

    # create a folder for watermarks if needed
    wm_dir = os.path.dirname(wm_path)
    if not os.path.exists(wm_dir):
        os.makedirs(wm_dir)

    img_path = get_path(url)

    if not os.path.exists(img_path):
        return url

    try:
        img = Image.open(img_path)

        mark = Image.open(watermark.mark.path)
        x = watermark.x or 0
        y = watermark.y or 0
        shift = (x, y)
        position = watermark.position

        opacity = watermark.opacity

        marked_img = make_watermark(img, mark, position, opacity, shift)
        marked_img.save(wm_path)
    except Exception, e:
        error("Cant create watermark for %s. Error type: %s. Msg: %s" % (img_path, type(e), e))
        return url

    if result_as_iff:
        return make_iff_instance(wm_path)

    return wm_url


def get_url_safe(path):
    """ If we save wm with result_as_iff == True, we thumbnail returns us full path to picture (not valid url)
    may be there is prettier way to manage this

    """

    if not path.startswith(settings.MEDIA_URL):
        return os.path.join(settings.MEDIA_URL, path.split(settings.MEDIA_URL)[-1])
    return path
