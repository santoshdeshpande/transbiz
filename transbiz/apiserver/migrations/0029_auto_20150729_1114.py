# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiserver', '0028_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industryvertical',
            name='logo_image',
            field=models.ImageField(upload_to=b'vertical_logo', null=True, verbose_name=b'Verical Logo', blank=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(null=True, upload_to=b'prod_image', blank=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product_id',
            field=models.ForeignKey(related_name='images', to='apiserver.Sale'),
        ),
    ]
