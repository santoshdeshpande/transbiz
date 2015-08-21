# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0046_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleresponse',
            name='cities',
        ),
        migrations.AddField(
            model_name='saleresponse',
            name='cities',
            field=models.ManyToManyField(to='apiserver.City'),
        ),
    ]
