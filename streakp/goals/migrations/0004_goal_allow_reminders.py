# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_auto_20150701_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='allow_reminders',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
