# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import django.utils.timezone
import model_utils.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0030_auto_20150729_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('questions', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, blank=True), size=None), size=None)),
                ('cities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
                ('qty_wanted', models.PositiveIntegerField(verbose_name=b'Quantity Wanted', validators=[django.core.validators.MinValueValidator(1)])),
                ('comments', models.CharField(max_length=200, blank=True)),
                ('product', models.ForeignKey(to='apiserver.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
