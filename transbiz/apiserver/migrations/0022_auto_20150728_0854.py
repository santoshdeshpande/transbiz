# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0021_auto_20150728_0722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='box_content',
            new_name='box_contents',
        ),
        migrations.RenameField(
            model_name='sale',
            old_name='startdate',
            new_name='start_date',
        ),
    ]
