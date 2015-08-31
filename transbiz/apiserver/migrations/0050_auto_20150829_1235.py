# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0049_auto_20150826_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='marked_products',
            field=models.ManyToManyField(related_name='sale_wishlist', to='apiserver.Sale'),
        ),
    ]
