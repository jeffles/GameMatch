# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default=1, unique=True, max_length=40),
            preserve_default=False,
        ),
    ]
