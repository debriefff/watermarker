# coding: utf-8
from django import template

from watermarker import core

register = template.Library()

register.filter(core.watermark)
register.filter(core.get_url_safe)
