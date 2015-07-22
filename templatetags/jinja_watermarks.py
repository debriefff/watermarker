# coding: utf-8
from django_jinja import library

from watermarker import core

library.filter(core.watermark)
library.filter(core.get_url_safe)
