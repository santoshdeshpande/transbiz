# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0049_buyresponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyrequest',
            name='category',
            field=models.ForeignKey(related_name='buy_requests', to='apiserver.Category'),
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='model',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='buyresponse',
            name='brand',
            field=models.ForeignKey(default=1, to='apiserver.Brand'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buyresponse',
            name='model',
            field=models.CharField(max_length=50),
        ),
    ]
