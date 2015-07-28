# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_default_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name='TransAdmin')
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Buyer')
    Group.objects.get_or_create(name='Seller')


class Migration(migrations.Migration):
    dependencies = [
        ('apiserver', '0007_auto_20150727_1444'),
    ]

    operations = [
        migrations.RunPython(create_default_groups)
    ]
