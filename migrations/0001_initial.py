# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Watermark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=32, verbose_name='Title')),
                ('mark', models.ImageField(upload_to=b'watermarks', verbose_name='Watermark')),
                ('opacity', models.FloatField(default=1, help_text='Value must be between 0 and 1', verbose_name='Opacity')),
                ('position', models.CharField(max_length=8, verbose_name='Position', choices=[(b'tile', 'tile'), (b'scale', 'scale'), (b'br', 'buttom right corner'), (b'tr', 'top rigth corner'), (b'bl', 'buttom left corner'), (b'tl', 'top left corner')])),
                ('x', models.IntegerField(default=0, null=True, verbose_name='Indent X', blank=True)),
                ('y', models.IntegerField(default=0, null=True, verbose_name='Indent Y', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('update_hard', models.BooleanField(default=False, help_text='Use it if you want to update all already created watermarks', verbose_name='Update hard')),
            ],
            options={
                'verbose_name': 'Watermark',
                'verbose_name_plural': 'Watermarks',
            },
            bases=(models.Model,),
        ),
    ]
