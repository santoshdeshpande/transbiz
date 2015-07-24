# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_default_company(apps, schema_editor):
    Company = apps.get_model("apiserver", "Company")
    State = apps.get_model("apiserver", "State")
    City = apps.get_model("apiserver", "City")

    state, result = State.objects.get_or_create(name='Karnataka', short_name='KA')
    city, result = City.objects.get_or_create(name="Bangalore", state=state)
    Company.objects.get_or_create(name='Optibiz', address_line_1='#30 II Floor IV Cross',
                                  address_line_2='Jayanagar VII Block', city=city, state=state, pin_code='560070',
                                  landline_number='080-23456789', tin='111111111', tan='22222222',
                                  service_tax_number='111111111')


class Migration(migrations.Migration):
    dependencies = [
        ('apiserver', '0003_auto_20150724_0640'),
    ]

    operations = [
        migrations.RunPython(create_default_company)
    ]
