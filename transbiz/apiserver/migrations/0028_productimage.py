# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0027_industryvertical_logo_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('image', models.ImageField(upload_to=b'prod_image')),
                ('order', models.PositiveIntegerField(default=0)),
                ('product_id', models.ForeignKey(to='apiserver.Sale')),
            ],
            options={
                'verbose_name': 'ProductImage',
                'verbose_name_plural': 'Product Images',
            },
        ),
    ]
