# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0004_goal_allow_reminders'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='goal',
            name='allow_reminders',
            field=models.BooleanField(default=False),
        ),
    ]
