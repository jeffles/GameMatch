# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField()),
                ('text', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_time', models.TimeField()),
                ('attendees', models.TextField()),
                ('location', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
