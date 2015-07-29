# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0029_auto_20150729_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='product_id',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='pushnotification',
            name='app_version',
            field=models.CharField(max_length=10),
        ),
    ]
