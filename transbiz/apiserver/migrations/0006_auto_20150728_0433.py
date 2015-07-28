# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0005_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=50, verbose_name=b'Name of the model'),
        ),
        migrations.AlterUniqueTogether(
            name='brand',
            unique_together=set([('name', 'category')]),
        ),
    ]
