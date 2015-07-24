# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('apiserver', '0001_initial')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20, verbose_name=b'Name of the State')),
                ('short_name', models.CharField(max_length=2, verbose_name=b'Short Name for the State(KA, MH etc)')),
            ],
        ),
    ]
