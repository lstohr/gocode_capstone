# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0002_auto_20150810_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='original_url',
            field=models.TextField(default='http://smittenkitchen.com/blog/2015/07/very-blueberry-scones/'),
            preserve_default=False,
        ),
    ]
