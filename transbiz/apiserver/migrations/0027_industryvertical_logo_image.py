# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0026_auto_20150729_0605'),
    ]

    operations = [
        migrations.AddField(
            model_name='industryvertical',
            name='logo_image',
            field=models.ImageField(null=True, upload_to=b'vertical_logo', blank=True),
        ),
    ]
