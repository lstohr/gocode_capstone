# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note_text', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=240)),
                ('instructions', models.TextField()),
                ('ingredients', models.TextField()),
                ('recipe_all', models.TextField()),
                ('category', models.CharField(max_length=120)),
                ('dish_type', models.CharField(default=b'Savory - side dish', max_length=8, choices=[(b'Sweet', b'Sweet'), (b'Savory - main dish', b'Savory - main dish'), (b'Savory - side dish', b'Savory - side dish')])),
            ],
        ),
        migrations.CreateModel(
            name='Cookbook_Items',
            fields=[
                ('recipe_id', models.OneToOneField(primary_key=True, serialize=False, to='cookbook.Recipe')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='recipe_id',
            field=models.ForeignKey(to='cookbook.Recipe'),
        ),
        migrations.AddField(
            model_name='note',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='note',
            name='cookbook_items_id',
            field=models.ForeignKey(to='cookbook.Cookbook_Items'),
        ),
    ]
