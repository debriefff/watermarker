from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Watermark(models.Model):
    OPACITY_ERROR_TEXT = _(u'Opacity should be more 0 and less 1. This is a rule!')

    TILE = 'tile'
    SCALE = 'scale'
    BR = 'br'
    TR = 'tr'
    BL = 'bl'
    TL = 'tl'

    POSITIONS = (
        (TILE, _(u'tile')),
        (SCALE, _(u'scale')),
        (BR, _(u'buttom right corner')),
        (TR, _(u'top rigth corner')),
        (BL, _(u'buttom left corner')),
        (TL, _(u'top left corner')),
    )

    title = models.CharField(max_length=32, verbose_name=_(u'Title'), unique=True)
    mark = models.ImageField(upload_to='watermarks', verbose_name=_(u'Watermark'))
    opacity = models.FloatField(default=1, verbose_name=_(u'Opacity'), help_text=_(u'Value must be between 0 and 1'))
    position = models.CharField(max_length=8, verbose_name=_(u'Position'), choices=POSITIONS)
    x = models.IntegerField(blank=True, null=True, verbose_name=_(u'Indent X'), default=0)
    y = models.IntegerField(blank=True, null=True, verbose_name=_(u'Indent Y'), default=0)
    is_active = models.BooleanField(default=True, verbose_name=_(u'Is active'))
    update_hard = models.BooleanField(default=False, verbose_name=_(u'Update hard'),
                                      help_text=_(u'Use it if you want to update all already created watermarks'))

    def get_position(self):
        return self.get_position_display()

    def clean(self):
        if not 0 <= self.opacity <= 1:
            raise ValidationError(self.OPACITY_ERROR_TEXT)

    def __unicode__(self):
        return self.title

    get_position.short_description = _(u'Position')

    class Meta:
        verbose_name = _(u'Watermark')
        verbose_name_plural = _(u'Watermarks')
