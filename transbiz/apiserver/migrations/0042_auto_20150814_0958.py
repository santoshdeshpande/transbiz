# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0041_auto_20150811_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='category',
            field=models.ForeignKey(related_name='sales', to='apiserver.Category'),
        ),
    ]
