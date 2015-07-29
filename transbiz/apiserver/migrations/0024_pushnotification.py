# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0023_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='PushNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('gcm_id', models.CharField(max_length=30)),
                ('imei_no', models.CharField(max_length=16)),
                ('phone_no', models.CharField(max_length=10, blank=True)),
                ('mobile_make', models.CharField(max_length=50)),
                ('mobile_model', models.CharField(max_length=50)),
                ('os_version', models.CharField(max_length=50)),
                ('app_version', models.DecimalField(verbose_name=b'Application Version', max_digits=5, decimal_places=3)),
                ('user', models.ForeignKey(to='apiserver.Brand')),
            ],
            options={
                'verbose_name': 'Push Notification',
                'verbose_name_plural': 'Push Notifications',
            },
        ),
    ]
