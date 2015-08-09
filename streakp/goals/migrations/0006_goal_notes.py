# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0005_auto_20150802_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='notes',
            field=models.TextField(null=True),
        ),
    ]
