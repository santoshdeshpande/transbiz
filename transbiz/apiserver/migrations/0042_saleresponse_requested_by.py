# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0041_auto_20150811_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleresponse',
            name='requested_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
