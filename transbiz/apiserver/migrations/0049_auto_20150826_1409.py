# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0048_buyrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyrequest',
            name='brand',
            field=models.ForeignKey(blank=True, to='apiserver.Brand', null=True),
        ),
    ]
