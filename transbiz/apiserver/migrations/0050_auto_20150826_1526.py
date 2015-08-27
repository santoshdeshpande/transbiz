# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0049_auto_20150826_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyrequest',
            name='delivery_date',
            field=models.DateTimeField(),
        ),
    ]
