# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0007_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sale',
            name='box_content',
            field=models.CharField(max_length=200, blank=b'True'),
        ),
        migrations.AddField(
            model_name='sale',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='sale',
            name='new',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='price_in_inr',
            field=models.PositiveIntegerField(default=False),
        ),
        migrations.AddField(
            model_name='sale',
            name='refurbished',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='shipped_to',
            field=models.ManyToManyField(to='apiserver.City'),
        ),
        migrations.AddField(
            model_name='sale',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='sale',
            name='warranty',
            field=models.PositiveIntegerField(default=False, verbose_name=b'Warranty in number of months'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='min_quantity',
            field=models.PositiveIntegerField(verbose_name=b'Minimum quantity', validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='sale',
            name='model',
            field=models.CharField(max_length=50),
        ),
    ]
