# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0048_buyrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('comments', models.CharField(max_length=200, blank=True)),
                ('model', models.CharField(max_length=50, blank=True)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('min_quantity', models.PositiveIntegerField(verbose_name=b'Minimum quantity', validators=[django.core.validators.MinValueValidator(1)])),
                ('unit_of_measure', models.CharField(max_length=10, choices=[(b'pcs', b'Pieces'), (b'pcks', b'Packs')])),
                ('price_in_inr', models.PositiveIntegerField(default=0)),
                ('new', models.BooleanField(default=True)),
                ('refurbished', models.BooleanField(default=True)),
                ('warranty', models.PositiveIntegerField(default=0, verbose_name=b'Warranty in number of months')),
                ('delivery_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('box_contents', models.CharField(max_length=200, blank=b'True')),
                ('brand', models.ForeignKey(blank=True, to='apiserver.Brand', null=True)),
                ('buy_request', models.ForeignKey(related_name='buy_request', to='apiserver.BuyRequest')),
                ('category', models.ForeignKey(related_name='buy_response', to='apiserver.Category')),
                ('company', models.ForeignKey(to='apiserver.Company')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('shipped_to', models.ManyToManyField(to='apiserver.City')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
