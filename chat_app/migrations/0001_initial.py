# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chat_id', models.CharField(max_length=10)),
                ('chat_name', models.TextField(default=b'Error')),
                ('username', models.TextField(null=True, blank=True)),
                ('message', models.TextField(null=True, blank=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('online_users', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
