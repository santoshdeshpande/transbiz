# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0006_auto_20150728_0433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('model', models.CharField(max_length=50, verbose_name=b'Model name of the product on sale')),
                ('description', models.CharField(max_length=200, blank=True)),
                ('min_quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('unit_of_measure', models.CharField(max_length=10, choices=[(b'pcs', b'Pieces'), (b'pcks', b'Packs')])),
                ('brand', models.ForeignKey(to='apiserver.Brand')),
                ('category', models.ForeignKey(to='apiserver.Category')),
                ('company', models.ForeignKey(to='apiserver.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
