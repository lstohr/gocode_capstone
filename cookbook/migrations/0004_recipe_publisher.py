# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0003_recipe_original_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='publisher',
            field=models.CharField(default='Smitten Kitchen', max_length=240),
            preserve_default=False,
        ),
    ]
