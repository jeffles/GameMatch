# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventbook', '0004_event_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('yearpublished', models.CharField(max_length=5)),
                ('minplayers', models.IntegerField()),
                ('maxplayers', models.IntegerField()),
                ('playingtime', models.CharField(max_length=50)),
                ('thumbnail', models.URLField()),
                ('image', models.URLField()),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
    ]
