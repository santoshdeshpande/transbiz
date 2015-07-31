# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import transbiz.apiserver.models


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0036_auto_20150731_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(null=True, upload_to=transbiz.apiserver.models.get_file_path, blank=True),
        ),
    ]
