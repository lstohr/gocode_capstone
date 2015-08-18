# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0004_recipe_publisher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='dish_type',
        ),
        migrations.AddField(
            model_name='note',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 22, 5, 18, 854356, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_id_from_api',
            field=models.CharField(default=b'empty', max_length=30),
        ),
    ]
