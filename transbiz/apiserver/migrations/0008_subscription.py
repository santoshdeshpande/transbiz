# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0007_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('company', models.ForeignKey(to='apiserver.Company')),
                ('plan', models.ForeignKey(to='apiserver.SubscriptionPlan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
