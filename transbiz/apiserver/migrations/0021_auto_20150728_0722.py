# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0020_auto_20150728_0717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='start_date',
            new_name='startdate',
        ),
    ]
