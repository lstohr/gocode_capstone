# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cookbook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cookbook_Item',
            fields=[
                ('recipe_id', models.OneToOneField(primary_key=True, serialize=False, to='cookbook.Recipe')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='cookbook_items',
            name='recipe_id',
        ),
        migrations.RemoveField(
            model_name='cookbook_items',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='note',
            name='cookbook_items_id',
        ),
        migrations.DeleteModel(
            name='Cookbook_Items',
        ),
        migrations.AddField(
            model_name='note',
            name='cookbook_item_id',
            field=models.ForeignKey(default=0, to='cookbook.Cookbook_Item'),
        ),
    ]
