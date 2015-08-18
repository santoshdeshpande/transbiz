# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0042_auto_20150814_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='vertical',
            field=models.ForeignKey(related_name='categories', to='apiserver.IndustryVertical'),
        ),
    ]
