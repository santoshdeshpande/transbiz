# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0009_auto_20150717_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='vertical',
            field=models.ForeignKey(default=None, to='apiserver.IndustryVertical'),
        ),
    ]
