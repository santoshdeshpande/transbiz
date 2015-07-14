# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0006_auto_20150714_0923'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('address_line_1', models.CharField(max_length=200)),
                ('address_line_2', models.CharField(max_length=200, blank=True)),
                ('pin_code', models.CharField(max_length=20)),
                ('landline_number', models.CharField(max_length=20)),
                ('tin', models.CharField(max_length=11, verbose_name=b'Tax-Payer Identification Number')),
                ('tan', models.CharField(max_length=10, verbose_name=b'Tax Deduction and Collection Account Number (TAN)')),
                ('service_tax_number', models.CharField(max_length=15)),
                ('ie_number', models.CharField(max_length=10, verbose_name=b'Import Export Code Number', blank=True)),
                ('website', models.URLField(blank=True)),
                ('active', models.BooleanField(default=False)),
                ('city', models.ForeignKey(to='apiserver.City')),
                ('state', models.ForeignKey(to='apiserver.State')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
    ]
